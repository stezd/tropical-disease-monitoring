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
    assert (data["engine"], data["fallback"]) == ("rules", False)


def test_score_preview_uses_rules(client: TestClient) -> None:
    r = client.post(f"{API}/flows/infection/score?preview=true", json=ANSWERS)
    assert r.status_code == 200
    assert r.json()["engine"] == "rules"


def test_read_flow_has_no_photo_step(client: TestClient) -> None:
    for flow_id in ("infection", "chronic"):
        data = client.get(f"{API}/flows/{flow_id}").json()
        assert "findings" not in data and "photo_analysis" not in data
        assert "q10" not in data["steps"]
        assert {"knee_r", "elbow_l", "shoulder_r"} <= {
            r["id"] for r in data["body_regions"]
        }


def test_score_rejects_bad_pain(client: TestClient) -> None:
    r = client.post(f"{API}/flows/infection/score", json={**ANSWERS, "pain": 60})
    assert r.status_code == 422


def test_save_needs_login(client: TestClient) -> None:
    r = client.post(
        f"{API}/screenings",
        json={"flow_id": "infection", "answers": ANSWERS, "consent": True},
    )
    assert r.status_code == 401


def test_save_needs_consent(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{API}/screenings",
        headers=normal_user_token_headers,
        json={"flow_id": "infection", "answers": ANSWERS, "consent": False},
    )
    assert r.status_code == 400


def test_save_screening(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    r = client.post(
        f"{API}/screenings",
        headers=normal_user_token_headers,
        json={"flow_id": "infection", "answers": ANSWERS, "consent": True},
    )
    assert r.status_code == 200
    assert r.json()["engine"] == "rules"
    rows = db.exec(select(Screening).where(Screening.top_disease == "malaria")).all()
    assert rows
    assert rows[-1].answers["pattern"] == "malaria"
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
