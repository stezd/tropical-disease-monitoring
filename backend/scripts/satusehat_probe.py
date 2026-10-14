# ruff: noqa: T201
"""Phase 0 probe for the SATUSEHAT integration.

Throwaway diagnostic, not part of the app. Answers three questions before we
build the Master Sarana Index mirror:

  1. Do the credentials work, and is the token shape what the docs claim?
  2. How often are facility coordinates null? "Nearest faskes" only works if
     MSI actually fills latitude/longitude -- the docs' own sample has them null.
  3. What jenis_sarana codes exist, and do province names match the front end
     (frontend/src/features/triage/location.ts)?

Read-only: writes nothing to SATUSEHAT, touches no database.

Run from backend/:

    uv run --env-file ../.env python scripts/satusehat_probe.py

Add --insecure if your network breaks TLS (the docs' curl examples all use it).
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter
from typing import Any

import httpx

SANDBOX = "https://api-satusehat-stg.dto.kemkes.go.id"
PRODUCTION = "https://api.satusehat.kemkes.go.id"
MSI_PATH = "/masterdata/v1/mastersaranaindex/mastersarana"

# The 38 provinces the front end knows about (location.ts). MSI returns its own
# names; --check-provinces flags any MSI name that is not in here.
FRONTEND_PROVINCES = {
    "Aceh",
    "Bali",
    "Banten",
    "Bengkulu",
    "DKI Jakarta",
    "Daerah Istimewa Yogyakarta",
    "Gorontalo",
    "Jambi",
    "Jawa Barat",
    "Jawa Tengah",
    "Jawa Timur",
    "Kalimantan Barat",
    "Kalimantan Selatan",
    "Kalimantan Tengah",
    "Kalimantan Timur",
    "Kalimantan Utara",
    "Kepulauan Bangka Belitung",
    "Kepulauan Riau",
    "Lampung",
    "Maluku",
    "Maluku Utara",
    "Nusa Tenggara Barat",
    "Nusa Tenggara Timur",
    "Papua",
    "Papua Barat",
    "Papua Barat Daya",
    "Papua Pegunungan",
    "Papua Selatan",
    "Papua Tengah",
    "Riau",
    "Sulawesi Barat",
    "Sulawesi Selatan",
    "Sulawesi Tengah",
    "Sulawesi Tenggara",
    "Sulawesi Utara",
    "Sumatera Barat",
    "Sumatera Selatan",
    "Sumatera Utara",
}


def head(title: str) -> None:
    print(f"\n{'=' * 68}\n{title}\n{'=' * 68}")


def blank(value: Any) -> bool:
    """MSI returns nulls, empty strings, and the literal string 'null'."""
    return value is None or value == "" or value == "null"


def get_token(
    client: httpx.Client, base: str, client_id: str, client_secret: str
) -> tuple[str, dict[str, Any]]:
    response = client.post(
        f"{base}/oauth2/v1/accesstoken",
        params={"grant_type": "client_credentials"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"client_id": client_id, "client_secret": client_secret},
    )
    if response.status_code != 200:
        raise SystemExit(
            f"\nAuth failed ({response.status_code}).\n{response.text[:600]}\n\n"
            "Check SATUSEHAT_CLIENT_ID / SATUSEHAT_CLIENT_SECRET, and that "
            "SATUSEHAT_ENV matches the environment they came from."
        )
    body = response.json()
    return body["access_token"], body


def fetch_page(
    client: httpx.Client,
    base: str,
    token: str,
    *,
    page: int = 1,
    limit: int = 2000,
    jenis: str | None = None,
    province: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {"limit": limit, "page": page}
    if jenis:
        params["jenis_sarana"] = jenis
    if province:
        params["kode_provinsi"] = province
    response = client.get(
        f"{base}{MSI_PATH}",
        params=params,
        headers={"Authorization": f"Bearer {token}"},
    )
    if response.status_code != 200:
        raise SystemExit(
            f"\nMSI request failed ({response.status_code}).\n{response.text[:600]}"
        )
    return response.json()


def report_token(body: dict[str, Any]) -> None:
    head("1. Token")
    raw_expires = body.get("expires_in")
    token = body.get("access_token", "")
    print(f"  access_token      : {token[:12]}... ({len(token)} chars)")
    print(f"  token_type        : {body.get('token_type')!r}")
    print(f"  expires_in        : {raw_expires!r}  (type {type(raw_expires).__name__})")
    print(f"  status            : {body.get('status')!r}")
    if not isinstance(raw_expires, str):
        print("  NOTE: docs say expires_in is a string; parse defensively anyway.")
    else:
        print("  Confirmed: expires_in is a string, as the docs show.")
    print(f"  organization_name : {body.get('organization_name')!r}")


def fetch_sample(
    client: httpx.Client, base: str, token: str, pages: int, limit: int
) -> tuple[list[dict[str, Any]], int]:
    rows: list[dict[str, Any]] = []
    total_pages = 0
    for page in range(1, pages + 1):
        body = fetch_page(client, base, token, page=page, limit=limit)
        total_pages = body.get("total_page") or 0
        batch = body.get("data") or []
        rows.extend(batch)
        print(f"  page {page}/{pages}: {len(batch)} rows (total_page={total_pages})")
        if len(batch) < limit:
            break
    return rows, total_pages


def report_quality(rows: list[dict[str, Any]]) -> None:
    head("2. Data quality (decides whether 'nearest faskes' is possible)")
    total = len(rows)
    if not total:
        print("  No rows returned. Nothing to measure.")
        return

    both = sum(
        1
        for r in rows
        if not blank(r.get("latitude")) and not blank(r.get("longitude"))
    )
    lat_only = sum(
        1 for r in rows if not blank(r.get("latitude")) and blank(r.get("longitude"))
    )
    print(f"  rows sampled          : {total}")
    print(f"  lat AND lon present   : {both} ({both * 100 // total}%)")
    print(f"  lat xor lon present   : {lat_only}")
    print(
        f"  coordinates missing   : {total - both} ({(total - both) * 100 // total}%)"
    )
    if both < total // 2:
        print(
            "\n  VERDICT: most facilities have no coordinates.\n"
            "  'Nearest faskes' degrades to 'listed in your province'. Still useful\n"
            "  for naming a real faskes + its kode_satusehat, but not for distance."
        )
    else:
        print("\n  VERDICT: coordinates are mostly present. Distance sort is viable.")

    for field in ("status_sarana", "status_aktif", "operasional"):
        counts = Counter(str(r.get(field)) for r in rows)
        print(f"\n  {field}:")
        for value, count in counts.most_common():
            print(f"    {value:<12} {count}")

    print(
        f"\n  rows with null 'alamat'  : {sum(1 for r in rows if blank(r.get('alamat')))}"
    )
    print(
        f"  rows with null 'telp'    : {sum(1 for r in rows if blank(r.get('telp')))}"
    )


def report_jenis(rows: list[dict[str, Any]]) -> None:
    head("3. jenis_sarana codes seen")
    counts: Counter[tuple[str, str]] = Counter()
    for row in rows:
        jenis = row.get("jenis_sarana") or {}
        counts[(str(jenis.get("kode")), str(jenis.get("nama")))] += 1
    for (kode, nama), count in sorted(counts.items()):
        print(f"    {kode:<8} {nama:<28} {count}")
    print("\n  Docs enumerate 101 Praktek Mandiri, 102 Puskesmas, 103 Klinik,")
    print("  104 Rumah Sakit (35 types exist). Check whether an Apotek code is")
    print("  above -- if not, the green route keeps today's Maps search.")


def report_provinces(rows: list[dict[str, Any]], check: bool) -> None:
    head("4. Province names (join key against location.ts)")
    seen: dict[str, str] = {}
    for row in rows:
        prov = row.get("provinsi") or {}
        nama, kode = prov.get("nama"), prov.get("kode")
        if nama and kode:
            seen[str(nama)] = str(kode)
    print(f"  {len(seen)} province name(s) in this sample:")
    for nama in sorted(seen):
        kode = seen[nama]
        flag = ""
        if check and nama not in FRONTEND_PROVINCES:
            flag = "   <-- NOT in location.ts PROVINCES"
        print(f"    {kode:<4} {nama}{flag}")
    if check:
        missing = FRONTEND_PROVINCES - set(seen)
        print(
            f"\n  {len(missing)} of the front end's 38 not in this sample "
            "(expected -- the sample is small). The real sync covers all."
        )


def probe_province_filter(
    client: httpx.Client, base: str, token: str, kode: str
) -> None:
    head(f"5. Province filter + payload size (kode_provinsi={kode})")
    body = fetch_page(client, base, token, page=1, limit=1, province=kode)
    total_pages = body.get("total_page") or 0
    total_rows = total_pages  # limit=1, so total_page == row count
    print(f"  total_page at limit=1 : {total_pages}  (~{total_rows} facilities)")
    print(f"  pages at limit=2000   : {(total_rows + 1999) // 2000}")
    for jenis, label in (("102", "Puskesmas"), ("104", "Rumah Sakit")):
        b = fetch_page(client, base, token, page=1, limit=1, province=kode, jenis=jenis)
        print(f"  {label:<12} : ~{b.get('total_page') or 0}")
    print("\n  This bounds the /api/v1/facilities response size in Phase 3.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--production", action="store_true", help="use Production host")
    parser.add_argument("--pages", type=int, default=2, help="MSI pages to sample")
    parser.add_argument(
        "--limit", type=int, default=2000, help="rows per page (max 2000)"
    )
    parser.add_argument(
        "--province", default="31", help="dagri code for the filter test"
    )
    parser.add_argument("--insecure", action="store_true", help="skip TLS verification")
    parser.add_argument(
        "--check-provinces", action="store_true", help="flag name drift"
    )
    args = parser.parse_args()

    client_id = os.environ.get("SATUSEHAT_CLIENT_ID", "").strip()
    client_secret = os.environ.get("SATUSEHAT_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        raise SystemExit(
            "Missing SATUSEHAT_CLIENT_ID / SATUSEHAT_CLIENT_SECRET.\n"
            "Fill them in .env, then run:\n"
            "  uv run --env-file ../.env python scripts/satusehat_probe.py"
        )

    base = PRODUCTION if args.production else SANDBOX
    env = "PRODUCTION" if args.production else "sandbox"
    print(f"SATUSEHAT Phase 0 probe  |  env={env}  |  {base}")

    with httpx.Client(timeout=30.0, verify=not args.insecure) as client:
        token, token_body = get_token(client, base, client_id, client_secret)
        report_token(token_body)

        head(f"MSI sample ({args.pages} page(s) x {args.limit})")
        rows, total_pages = fetch_sample(client, base, token, args.pages, args.limit)
        print(f"  sampled {len(rows)} rows")
        if total_pages:
            print(
                f"  national total_page={total_pages} at limit={args.limit} "
                f"(~{total_pages * args.limit:,} facilities)"
            )

        report_quality(rows)
        report_jenis(rows)
        report_provinces(rows, args.check_provinces)
        probe_province_filter(client, base, token, args.province)

    head("Done")
    print("  No writes were made. Nothing was saved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
