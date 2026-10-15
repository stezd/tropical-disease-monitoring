"""POST /facilities/nearest: distance ranking with a data-quality tie-break."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine
from app.models import Facility

API = f"{settings.API_V1_STR}/facilities/nearest"

# The point every distance below is measured from.
HERE = {"latitude": -6.2, "longitude": 106.8}


def _facility(**overrides: object) -> Facility:
    defaults: dict[str, object] = {
        "satusehat_id": "2000000001",
        "code": "P3100000001",
        "name": "Puskesmas Contoh",
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


def test_empty_db_returns_empty_list(client: TestClient) -> None:
    r = client.post(API, json=HERE)
    assert r.status_code == 200
    assert r.json() == {"data": [], "count": 0}


@pytest.fixture(scope="module")
def seeded() -> Generator[None]:
    with Session(engine) as session:
        session.add_all(
            [
                # 0.0 km away, but no contact details at all (quality 0).
                _facility(
                    satusehat_id="2000000001",
                    code="P3100000001",
                    name="Puskesmas Dekat Tanpa Kontak",
                    city_name="Jakarta Pusat",
                ),
                # ~0.1 km away: same distance band, full contact details and
                # MSI-verified, so it should outrank the one above.
                _facility(
                    satusehat_id="2000000002",
                    code="P3100000002",
                    name="Puskesmas Dekat Lengkap",
                    city_name="Jakarta Pusat",
                    address="Jl. Contoh No. 1",
                    phone="0211234567",
                    status_sarana="verified",
                    latitude=-6.2009,
                ),
                # ~2 km away: further than the tie band, so it comes last.
                _facility(
                    satusehat_id="2000000003",
                    code="P3100000003",
                    name="Puskesmas Agak Jauh",
                    phone="0219999999",
                    latitude=-6.218,
                ),
                # No coordinates: cannot be distance-sorted, always skipped.
                _facility(
                    satusehat_id="2000000004",
                    code="P3100000004",
                    name="Puskesmas Tanpa Koordinat",
                    latitude=None,
                    longitude=None,
                ),
                # Non-operational: must never appear.
                _facility(
                    satusehat_id="2000000005",
                    code="P3100000005",
                    name="Puskesmas Tutup",
                    operational=False,
                ),
                # A hospital far away, for the kind filter.
                _facility(
                    satusehat_id="2000000006",
                    code="P3400000001",
                    name="RSUD Jauh",
                    jenis_sarana_kode="104",
                    jenis_sarana_nama="Rumah Sakit",
                    province_code="34",
                    province_name="Yogyakarta",
                    latitude=-7.79,
                    longitude=110.36,
                ),
            ]
        )
        session.commit()
    yield


@pytest.mark.usefixtures("seeded")
def test_near_tie_prefers_better_data(client: TestClient) -> None:
    r = client.post(API, json={**HERE, "limit": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    # 0.0 km and 0.1 km are inside the same tie band: the complete record wins.
    assert [f["name"] for f in body["data"]] == [
        "Puskesmas Dekat Lengkap",
        "Puskesmas Dekat Tanpa Kontak",
    ]
    assert body["data"][0]["distance_km"] == pytest.approx(0.1, abs=0.02)
    assert body["data"][1]["distance_km"] == 0.0


@pytest.mark.usefixtures("seeded")
def test_skips_rows_without_coordinates(client: TestClient) -> None:
    r = client.post(API, json={**HERE, "limit": 20})
    assert r.status_code == 200
    names = {f["name"] for f in r.json()["data"]}
    assert "Puskesmas Tanpa Koordinat" not in names
    assert "Puskesmas Tutup" not in names
    # The distant hospital is still reachable once the limit is wide enough.
    assert "RSUD Jauh" in names


@pytest.mark.usefixtures("seeded")
def test_filter_by_kind(client: TestClient) -> None:
    r = client.post(API, json={**HERE, "kind": "rs", "limit": 5})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["data"][0]["name"] == "RSUD Jauh"


@pytest.mark.usefixtures("seeded")
def test_limit_is_respected(client: TestClient) -> None:
    r = client.post(API, json={**HERE, "limit": 1})
    assert r.status_code == 200
    assert r.json()["count"] == 1


@pytest.mark.usefixtures("seeded")
def test_distance_orders_beyond_the_tie_band(client: TestClient) -> None:
    r = client.post(API, json={**HERE, "kind": "puskesmas", "limit": 3})
    distances = [f["distance_km"] for f in r.json()["data"]]
    # Further than the tie band: strictly last. The two near ones are inside the
    # band, so their order is decided by data quality, not by metres.
    assert distances[-1] == 2.0
    assert set(distances[:2]) == {0.0, 0.1}


def test_out_of_range_coordinates_are_rejected(client: TestClient) -> None:
    assert (
        client.post(API, json={"latitude": 200, "longitude": 106.8}).status_code == 422
    )
    assert (
        client.post(API, json={"latitude": -6.2, "longitude": 999}).status_code == 422
    )


def test_limit_bounds_are_rejected(client: TestClient) -> None:
    assert client.post(API, json={**HERE, "limit": 0}).status_code == 422
    assert client.post(API, json={**HERE, "limit": 21}).status_code == 422
