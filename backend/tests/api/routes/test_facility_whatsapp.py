"""Curated WhatsApp numbers: the admin endpoint and sync safety."""

import importlib.util
from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, select

from app.core.config import settings
from app.core.db import engine
from app.models import Facility

API = f"{settings.API_V1_STR}/facilities"

# Import the sync script (backend/scripts is not a package) to prove a re-sync
# does not clobber a curated number.
_SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "sync_facilities.py"
_spec = importlib.util.spec_from_file_location("sync_facilities", _SCRIPT)
assert _spec and _spec.loader
sync_facilities = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sync_facilities)


def _facility(**overrides: object) -> Facility:
    defaults: dict[str, object] = {
        "satusehat_id": "3000000001",
        "code": "P3100000001",
        "name": "Puskesmas Kurasi",
        "jenis_sarana_kode": "102",
        "jenis_sarana_nama": "Pusat Kesehatan Masyarakat",
        "province_code": "31",
        "province_name": "DKI Jakarta",
        "latitude": -6.2,
        "longitude": 106.8,
    }
    return Facility(**{**defaults, **overrides})


@pytest.fixture(scope="module", autouse=True)
def clean_facilities() -> Generator[None]:
    with Session(engine) as session:
        session.execute(delete(Facility))
        session.commit()
    yield
    with Session(engine) as session:
        session.execute(delete(Facility))
        session.commit()


@pytest.fixture(scope="module")
def one_facility() -> Generator[None]:
    with Session(engine) as session:
        session.add(_facility())
        session.commit()
    yield


@pytest.mark.usefixtures("one_facility")
def test_requires_superuser(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    url = f"{API}/3000000001/whatsapp"
    # No token, then a plain user: neither may curate.
    assert client.put(url, json={"wa_number": "08123456789"}).status_code in (401, 403)
    r = client.put(
        url, json={"wa_number": "08123456789"}, headers=normal_user_token_headers
    )
    assert r.status_code == 403


@pytest.mark.usefixtures("one_facility")
def test_superuser_sets_normalized_number(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.put(
        f"{API}/3000000001/whatsapp",
        json={"wa_number": "0812-3456-7890"},
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["wa_number"] == "6281234567890"


@pytest.mark.usefixtures("one_facility")
def test_plus62_is_accepted(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.put(
        f"{API}/3000000001/whatsapp",
        json={"wa_number": "+62 812 3456 7890"},
        headers=superuser_token_headers,
    )
    assert r.status_code == 200
    assert r.json()["wa_number"] == "6281234567890"


@pytest.mark.usefixtures("one_facility")
def test_landline_is_rejected(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.put(
        f"{API}/3000000001/whatsapp",
        json={"wa_number": "021-3842828"},
        headers=superuser_token_headers,
    )
    assert r.status_code == 422


@pytest.mark.usefixtures("one_facility")
def test_null_clears(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    url = f"{API}/3000000001/whatsapp"
    client.put(url, json={"wa_number": "08123456789"}, headers=superuser_token_headers)
    r = client.put(url, json={"wa_number": None}, headers=superuser_token_headers)
    assert r.status_code == 200
    assert r.json()["wa_number"] is None


def test_unknown_facility_is_404(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.put(
        f"{API}/does-not-exist/whatsapp",
        json={"wa_number": "08123456789"},
        headers=superuser_token_headers,
    )
    assert r.status_code == 404


@pytest.mark.usefixtures("one_facility")
def test_sync_does_not_wipe_curated_number(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    client.put(
        f"{API}/3000000001/whatsapp",
        json={"wa_number": "08123456789"},
        headers=superuser_token_headers,
    )

    # A fresh MSI row for the same facility, exactly as the cron would send it.
    raw: dict[str, Any] = {
        "kode_satusehat": "3000000001",
        "kode_sarana": "P3100000001",
        "nama": "Puskesmas Kurasi (nama baru)",
        "jenis_sarana": {"kode": "102", "nama": "Pusat Kesehatan Masyarakat"},
        "provinsi": {"kode": "31", "nama": "DKI Jakarta"},
        "latitude": -6.21,
        "longitude": 106.81,
        "operasional": True,
        "status_sarana": "verified",
    }
    record = sync_facilities.parse_facility_row(raw, datetime.now(UTC))
    assert record is not None
    assert "wa_number" not in record  # the sync never writes this column

    with Session(engine) as session:
        sync_facilities.upsert_facilities(session, [record])
        row = session.exec(
            select(Facility).where(Facility.satusehat_id == "3000000001")
        ).one()

    assert row.name == "Puskesmas Kurasi (nama baru)"  # MSI fields refreshed
    assert row.wa_number == "628123456789"  # curated number preserved
