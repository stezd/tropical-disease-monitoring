import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models import Screening, ScreeningStat

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
    client: TestClient,
    db: Session,
    normal_user_token_headers: dict[str, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Pin the rule engine. A developer with TRIAGE_SCORING_ENGINE=ai in .env would
    # otherwise get "ai" (or "ai-fb:timeout") here; CI has no .env at all.
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "rules")
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
    # The engine that actually produced the scores.
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


# --- statistics without direct identity -------------------------------------------


def _stat_body(
    event_id: uuid.UUID | None = None, **answers: object
) -> dict[str, object]:
    return {
        "event_id": str(event_id or uuid.uuid4()),
        "flow_id": "infection",
        "answers": {**ANSWERS, **answers},
    }


def _rows(db: Session, event_id: str) -> list[ScreeningStat]:
    db.expire_all()
    return list(
        db.exec(
            select(ScreeningStat).where(ScreeningStat.event_id == uuid.UUID(event_id))
        ).all()
    )


@pytest.fixture
def rules_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "rules")


@pytest.mark.usefixtures("clean_screening_stats", "rules_engine")
def test_stats_guest_writes_one_row(client: TestClient, db: Session) -> None:
    body = _stat_body(drugs="paracetamol RAHASIA", province="Papua")
    r = client.post(f"{API}/stats", json=body)
    assert r.status_code == 204
    assert r.content == b""
    (row,) = _rows(db, str(body["event_id"]))
    assert row.top_disease == "malaria"
    assert row.route == "yellow"
    assert row.age_band == "25-44"
    assert row.province == "Papua"
    assert row.drugs_given is True
    dump = repr(row.model_dump())
    for needle in ("RAHASIA", "38.6", "'age'", "weight", "height"):
        assert needle not in dump
    assert row.day == datetime.now(ZoneInfo("Asia/Jakarta")).date()


@pytest.mark.usefixtures("clean_screening_stats", "rules_engine")
def test_stats_same_event_id_updates_row(client: TestClient, db: Session) -> None:
    eid = uuid.uuid4()
    assert client.post(f"{API}/stats", json=_stat_body(eid)).status_code == 204
    assert (
        client.post(f"{API}/stats", json=_stat_body(eid, province="Bali")).status_code
        == 204
    )
    (row,) = _rows(db, str(eid))
    assert row.province == "Bali"


@pytest.mark.usefixtures("clean_screening_stats", "rules_engine")
def test_stats_logged_in_user_is_not_linked(
    client: TestClient,
    db: Session,
    normal_user_token_headers: dict[str, str],
) -> None:
    body = _stat_body()
    r = client.post(f"{API}/stats", headers=normal_user_token_headers, json=body)
    assert r.status_code == 204
    (row,) = _rows(db, str(body["event_id"]))
    assert "user_id" not in ScreeningStat.model_fields
    assert not any(
        "user" in k or "email" in k or "created" in k for k in row.model_dump()
    )


@pytest.mark.usefixtures("clean_screening_stats", "rules_engine")
def test_stats_red_flag_is_red(client: TestClient, db: Session) -> None:
    body = _stat_body(red_flags=["syok"])
    assert client.post(f"{API}/stats", json=body).status_code == 204
    (row,) = _rows(db, str(body["event_id"]))
    assert row.route == "red"
    assert row.red_flags == ["syok"]


def test_stats_rejects_bad_input(client: TestClient) -> None:
    assert (
        client.post(f"{API}/stats", json={**_stat_body(), "event_id": "x"}).status_code
        == 422
    )
    assert (
        client.post(
            f"{API}/stats", json={**_stat_body(), "flow_id": "nope"}
        ).status_code
        == 404
    )


@pytest.mark.usefixtures("clean_screening_stats", "rules_engine")
def test_stats_summary_superuser_only_and_small_cells(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    normal_user_token_headers: dict[str, str],
) -> None:
    url = f"{API}/stats/summary"
    assert client.get(url).status_code == 401
    assert client.get(url, headers=normal_user_token_headers).status_code == 403

    for _ in range(10):
        assert (
            client.post(f"{API}/stats", json=_stat_body(province="Papua")).status_code
            == 204
        )
    for _ in range(3):
        assert (
            client.post(f"{API}/stats", json=_stat_body(province="Bali")).status_code
            == 204
        )
    for period in ("day", "week"):
        r = client.get(url, headers=superuser_token_headers, params={"period": period})
        assert r.status_code == 200
        data = r.json()
        assert data["k"] == 10
        by_province = {row["province"]: row["count"] for row in data["data"]}
        assert by_province == {"Papua": 10, "Bali": None}
    r = client.get(url, headers=superuser_token_headers, params={"period": "year"})
    assert r.status_code == 422
