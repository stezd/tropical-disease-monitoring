# ruff: noqa: T201
"""Sync health facilities from SATUSEHAT Master Sarana Index (MSI).

Fetches operational Puskesmas (102) and Rumah Sakit (104) from SATUSEHAT and
mirrors them into the local PostgreSQL `facility` table. Apotek (105) is opt-in
with --include-apotek; see DEFAULT_JENIS for why.

Run from backend/:
    uv run --env-file ../.env python scripts/sync_facilities.py
    uv run --env-file ../.env python scripts/sync_facilities.py --province 31
    uv run --env-file ../.env python scripts/sync_facilities.py --include-apotek
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from typing import Any

import httpx
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session

from app.core.config import settings
from app.core.db import engine
from app.models import Facility

MSI_PATH = "/masterdata/v1/mastersaranaindex/mastersarana"
# Default: Puskesmas (102) and Rumah Sakit (104). Both have ~96-100% coordinate
# coverage. Apotek (105) is opt-in via --include-apotek because only 2.1% of
# apotek rows in MSI have coordinates, so they cannot be distance-sorted.
DEFAULT_JENIS = ("102", "104")
ALL_JENIS = ("102", "104", "105")


def _is_blank(value: Any) -> bool:
    return value is None or value == "" or value == "null"


def _clean_str(value: Any, max_len: int | None = None) -> str | None:
    if _is_blank(value):
        return None
    s = str(value).strip()
    return s[:max_len] if max_len else s


def _clean_coord(value: Any) -> float | None:
    if _is_blank(value):
        return None
    try:
        f = float(value)
        return f if f == f else None  # filter NaN
    except ValueError, TypeError:
        return None


def get_token(
    client: httpx.Client, base: str, client_id: str, client_secret: str
) -> str:
    response = client.post(
        f"{base}/oauth2/v1/accesstoken",
        params={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"client_id": client_id, "client_secret": client_secret},
    )
    if response.status_code != 200:
        raise SystemExit(
            f"SATUSEHAT auth failed ({response.status_code}):\n{response.text[:500]}"
        )
    return str(response.json()["access_token"])


def fetch_page(
    client: httpx.Client,
    base: str,
    token: str,
    *,
    page: int,
    limit: int,
    kinds: Sequence[str] = DEFAULT_JENIS,
    province: str | None = None,
) -> dict[str, Any]:
    params: list[tuple[str, str | int | float | bool | None]] = [
        ("status_aktif", "true"),
        ("limit", str(limit)),
        ("page", str(page)),
    ]
    for jenis in kinds:
        params.append(("jenis_sarana", jenis))
    if province:
        params.append(("kode_provinsi", province.strip()))

    response = client.get(
        f"{base}{MSI_PATH}",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise SystemExit(
            f"MSI request failed on page {page} ({response.status_code}):\n{response.text[:500]}"
        )
    body: dict[str, Any] = response.json()
    return body


def parse_facility_row(raw: dict[str, Any], now: datetime) -> dict[str, Any] | None:
    satusehat_id = _clean_str(raw.get("kode_satusehat"), 64)
    code = _clean_str(raw.get("kode_sarana"), 64)
    name = _clean_str(raw.get("nama"), 255)
    if not satusehat_id or not code or not name:
        return None

    jenis = raw.get("jenis_sarana") or {}
    prov = raw.get("provinsi") or {}
    kabkota = raw.get("kabkota") or {}

    jenis_kode = _clean_str(jenis.get("kode"), 10) or ""
    jenis_nama = _clean_str(jenis.get("nama"), 100) or ""
    prov_kode = _clean_str(prov.get("kode"), 10) or ""
    prov_nama = _clean_str(prov.get("nama"), 100) or ""
    # The API requires a province (min_length=2), so a row without one could
    # never be returned by any query. MSI ships a handful of these nationally.
    if not prov_kode or not prov_nama:
        return None

    operational_raw = raw.get("operasional")
    operational = (
        True
        if _is_blank(operational_raw)
        else str(operational_raw).strip().lower() == "true"
    )

    lat = _clean_coord(raw.get("latitude"))
    lon = _clean_coord(raw.get("longitude"))
    # (0, 0) is MSI's placeholder for missing coordinates (Null Island).
    if lat == 0.0 and lon == 0.0:
        lat, lon = None, None

    return {
        "satusehat_id": satusehat_id,
        "code": code,
        "name": name,
        "jenis_sarana_kode": jenis_kode,
        "jenis_sarana_nama": jenis_nama,
        "province_code": prov_kode,
        "province_name": prov_nama,
        "city_name": _clean_str(kabkota.get("nama"), 100),
        "address": _clean_str(raw.get("alamat"), 500),
        "phone": _clean_str(raw.get("telp"), 100),
        "latitude": lat,
        "longitude": lon,
        "operational": operational,
        "status_sarana": _clean_str(raw.get("status_sarana"), 50),
        "updated_at": now,
    }


def upsert_facilities(session: Session, records: list[dict[str, Any]]) -> int:
    if not records:
        return 0

    stmt = pg_insert(Facility).values(records)
    stmt = stmt.on_conflict_do_update(
        index_elements=[Facility.satusehat_id],
        set_={
            "code": stmt.excluded.code,
            "name": stmt.excluded.name,
            "jenis_sarana_kode": stmt.excluded.jenis_sarana_kode,
            "jenis_sarana_nama": stmt.excluded.jenis_sarana_nama,
            "province_code": stmt.excluded.province_code,
            "province_name": stmt.excluded.province_name,
            "city_name": stmt.excluded.city_name,
            "address": stmt.excluded.address,
            "phone": stmt.excluded.phone,
            "latitude": stmt.excluded.latitude,
            "longitude": stmt.excluded.longitude,
            "operational": stmt.excluded.operational,
            "status_sarana": stmt.excluded.status_sarana,
            "updated_at": stmt.excluded.updated_at,
        },
    )
    session.exec(stmt)
    session.commit()
    return len(records)


def sync_msi(
    *,
    limit: int = 1000,
    max_pages: int | None = None,
    province: str | None = None,
    kinds: Sequence[str] = DEFAULT_JENIS,
    insecure: bool = False,
) -> int:
    client_id = settings.SATUSEHAT_CLIENT_ID.strip()
    client_secret = settings.SATUSEHAT_CLIENT_SECRET.strip()
    if not client_id or not client_secret:
        raise SystemExit(
            "Missing SATUSEHAT_CLIENT_ID or SATUSEHAT_CLIENT_SECRET in environment.\n"
            "Set them in .env before running sync."
        )

    base = settings.satusehat_base_url
    print(f"Connecting to SATUSEHAT MSI ({settings.SATUSEHAT_ENV}): {base}")

    total_synced = 0
    now = datetime.now(UTC)

    with httpx.Client(timeout=60.0, verify=not insecure) as http_client:
        token = get_token(http_client, base, client_id, client_secret)
        print("Obtained SATUSEHAT OAuth2 access token.")

        page = 1
        with Session(engine) as session:
            while True:
                if max_pages and page > max_pages:
                    break

                body = fetch_page(
                    http_client,
                    base,
                    token,
                    page=page,
                    limit=limit,
                    kinds=kinds,
                    province=province,
                )
                raw_rows: list[dict[str, Any]] = body.get("data") or []
                total_page: int = body.get("total_page") or 0

                records = []
                for row in raw_rows:
                    # Docs (SATUSEHAT.md): keep verified/valid, drop draft/review.
                    status = str(row.get("status_sarana") or "").strip().lower()
                    if status in {"draft", "review"}:
                        continue
                    rec = parse_facility_row(row, now)
                    if rec is not None:
                        records.append(rec)

                upserted = upsert_facilities(session, records)
                total_synced += upserted

                print(
                    f"Page {page}/{total_page or '?'}: "
                    f"read {len(raw_rows)} rows, upserted {upserted} facilities "
                    f"(cumulative: {total_synced})"
                )

                if len(raw_rows) < limit or (total_page and page >= total_page):
                    break
                page += 1

    print(f"Sync complete. Total facilities synced: {total_synced}")
    return total_synced


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="rows per page. MSI documents 2000, but the Apigee gateway returns "
        "502 TooBigBody above ~1500 (measured), so 1000 leaves margin",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="maximum number of pages to sync (default: all)",
    )
    parser.add_argument(
        "--province",
        type=str,
        default=None,
        help="filter by provincial dagri code, e.g. 31 (DKI Jakarta)",
    )
    parser.add_argument(
        "--include-apotek",
        action="store_true",
        help="also sync Apotek (105). Off by default: almost no apotek rows in "
        "MSI carry coordinates, so they cannot be distance-sorted",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="skip TLS verification if network proxies break certs",
    )
    args = parser.parse_args()

    kinds = ALL_JENIS if args.include_apotek else DEFAULT_JENIS
    sync_msi(
        limit=args.limit,
        max_pages=args.max_pages,
        province=args.province,
        kinds=kinds,
        insecure=args.insecure,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
