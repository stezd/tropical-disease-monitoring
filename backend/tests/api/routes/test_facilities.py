from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.config import settings
from app.core.db import engine
from app.models import Facility

API = f"{settings.API_V1_STR}/facilities"


def _facility(**overrides: object) -> Facility:
    defaults: dict[str, object] = {
        "satusehat_id": "1000000001",
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
    r = client.get(f"{API}/", params={"province": "DKI Jakarta"})
    assert r.status_code == 200
    assert r.json() == {"data": [], "count": 0}


@pytest.fixture(scope="module")
def seeded() -> Generator[None]:
    with Session(engine) as session:
        session.add_all(
            [
                # Puskesmas with coordinates (should sort first).
                _facility(
                    satusehat_id="1000000001",
                    code="P3100000001",
                    name="Puskesmas Menteng",
                    jenis_sarana_kode="102",
                    jenis_sarana_nama="Pusat Kesehatan Masyarakat",
                    province_code="31",
                    province_name="DKI Jakarta",
                    city_name="Jakarta Pusat",
                    latitude=-6.19,
                    longitude=106.83,
                ),
                # Puskesmas without coordinates (sorts after the one above).
                _facility(
                    satusehat_id="1000000002",
                    code="P3100000002",
                    name="Puskesmas Tanpa Koordinat",
                    province_code="31",
                    province_name="DKI Jakarta",
                    latitude=None,
                    longitude=None,
                ),
                # Non-operational: must never appear.
                _facility(
                    satusehat_id="1000000003",
                    code="P3100000003",
                    name="Puskesmas Tutup",
                    province_code="31",
                    province_name="DKI Jakarta",
                    operational=False,
                ),
                # Rumah sakit in Yogyakarta, stored under MSI's name.
                _facility(
                    satusehat_id="1000000004",
                    code="P3400000001",
                    name="RSUD Yogyakarta",
                    jenis_sarana_kode="104",
                    jenis_sarana_nama="Rumah Sakit",
                    province_code="34",
                    province_name="Yogyakarta",
                    latitude=-7.79,
                    longitude=110.36,
                ),
                # Apotek in Yogyakarta.
                _facility(
                    satusehat_id="1000000005",
                    code="P3400000002",
                    name="Apotek Sehat",
                    jenis_sarana_kode="105",
                    jenis_sarana_nama="Apotek",
                    province_code="34",
                    province_name="Yogyakarta",
                ),
            ]
        )
        session.commit()
    yield


@pytest.mark.usefixtures("seeded")
def test_filter_by_province_name(client: TestClient) -> None:
    r = client.get(f"{API}/", params={"province": "DKI Jakarta"})
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 2
    # Coordinates-first ordering: the one with lat/lon comes first.
    assert [f["name"] for f in body["data"]] == [
        "Puskesmas Menteng",
        "Puskesmas Tanpa Koordinat",
    ]
    assert body["data"][0]["latitude"] == -6.19


@pytest.mark.usefixtures("seeded")
def test_filter_by_province_code(client: TestClient) -> None:
    r = client.get(f"{API}/", params={"province": "31"})
    assert r.status_code == 200
    assert r.json()["count"] == 2


@pytest.mark.usefixtures("seeded")
def test_filter_by_kind_label(client: TestClient) -> None:
    r = client.get(f"{API}/", params={"province": "DKI Jakarta", "kind": "puskesmas"})
    assert r.status_code == 200
    assert r.json()["count"] == 2

    r = client.get(f"{API}/", params={"province": "DKI Jakarta", "kind": "rs"})
    assert r.status_code == 200
    assert r.json()["count"] == 0


@pytest.mark.usefixtures("seeded")
def test_filter_by_kind_code(client: TestClient) -> None:
    r = client.get(f"{API}/", params={"province": "DKI Jakarta", "kind": "102"})
    assert r.status_code == 200
    assert r.json()["count"] == 2


@pytest.mark.usefixtures("seeded")
def test_yogyakarta_alias(client: TestClient) -> None:
    for province in ("Yogyakarta", "Daerah Istimewa Yogyakarta", "34"):
        r = client.get(f"{API}/", params={"province": province})
        assert r.status_code == 200, province
        body = r.json()
        assert body["count"] == 2, province
        assert {f["name"] for f in body["data"]} == {"RSUD Yogyakarta", "Apotek Sehat"}

    r = client.get(
        f"{API}/",
        params={"province": "Daerah Istimewa Yogyakarta", "kind": "rs"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["data"][0]["name"] == "RSUD Yogyakarta"


def test_province_too_short_is_rejected(client: TestClient) -> None:
    r = client.get(f"{API}/", params={"province": "3"})
    assert r.status_code == 422


def test_missing_province_is_rejected(client: TestClient) -> None:
    assert client.get(f"{API}/").status_code == 422
