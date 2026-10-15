from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import Screening

API = f"{settings.API_V1_STR}/triage"

ANSWERS = {
    "who": "self",
    "age": 25,
    "sex": "P",
    "red_flags": ["none"],
    "complaint": "A",
    "pattern": "malaria",
    "companion": ["malaria"],
    "eco": ["timur"],
    "temp": 38.6,
    "height_cm": 160,
    "weight_kg": 52,
    "body": [],
    "findings": [],
}


def test_read_flow(client: TestClient) -> None:
    r = client.get(f"{API}/flows/infection")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "infection"
    assert {f["id"] for f in data["red_flags"]} >= {"syok", "rabies"}
    assert data["diseases"]["dbd"]["route"] == "yellow"
    assert "weights" not in data
    assert "lab" not in data["diseases"]["dbd"]


def test_read_chronic_flow(client: TestClient) -> None:
    r = client.get(f"{API}/flows/chronic")
    assert r.status_code == 200
    data = r.json()
    assert data["vitals"] == ["bp", "glucose"]
    assert {f["id"] for f in data["red_flags"]} >= {"syok", "stroke"}


def test_read_unknown_flow(client: TestClient) -> None:
    assert client.get(f"{API}/flows/nope").status_code == 404


def test_score(client: TestClient) -> None:
    r = client.post(f"{API}/flows/infection/score", json=ANSWERS)
    assert r.status_code == 200
    data = r.json()
    assert data["top"]["id"] == "malaria"
    assert data["route"] == "yellow"
    assert data["summary"].startswith("TROPICARE")


def test_score_rejects_bad_pain(client: TestClient) -> None:
    r = client.post(f"{API}/flows/infection/score", json={**ANSWERS, "pain": 60})
    assert r.status_code == 422


def test_save_needs_consent(client: TestClient) -> None:
    r = client.post(
        f"{API}/screenings",
        json={"flow_id": "infection", "answers": ANSWERS, "consent": False},
    )
    assert r.status_code == 400


def test_save_screening(client: TestClient, db: Session) -> None:
    r = client.post(
        f"{API}/screenings",
        json={"flow_id": "infection", "answers": ANSWERS, "consent": True},
    )
    assert r.status_code == 200
    rows = db.exec(select(Screening).where(Screening.top_disease == "malaria")).all()
    assert rows
    assert rows[-1].answers["pattern"] == "malaria"
    # The engine that actually produced the scores (default config: rules).
    assert rows[-1].engine == "rules"


def test_list_screenings_superuser_only(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    assert client.get(f"{API}/screenings").status_code == 401
    r = client.get(f"{API}/screenings", headers=normal_user_token_headers)
    assert r.status_code == 403
    r = client.get(f"{API}/screenings", headers=superuser_token_headers)
    assert r.status_code == 200
    assert "count" in r.json()


def test_photo_analysis_not_available(client: TestClient) -> None:
    r = client.post(
        f"{API}/photo/analyze",
        files={"photo": ("x.jpg", b"not really a photo", "image/jpeg")},
    )
    assert r.status_code == 200
    assert r.json() == {
        "available": False,
        "findings": [],
        "message": "Analisis foto belum tersedia.",
    }
