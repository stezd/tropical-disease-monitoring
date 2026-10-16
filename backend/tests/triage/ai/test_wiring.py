import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, col, select

from app.api.deps import get_current_active_superuser
from app.api.routes import ai as ai_route
from app.composition import triage_container
from app.core.config import settings
from app.domain.answers import Answers
from app.main import app
from app.models import Screening
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine
from app.triage.ai.llm import LLMReply, LLMServerError
from app.triage.content import get_content
from tests.triage.ai.test_engine import MALARIA


@pytest.fixture
def as_admin() -> Any:
    """Skip the login for the admin-only /ai endpoints."""
    app.dependency_overrides[get_current_active_superuser] = lambda: None
    yield
    app.dependency_overrides.pop(get_current_active_superuser, None)


class OneShot:
    model = "fake-model"

    def __init__(self) -> None:
        self.calls = 0

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        self.calls += 1
        text = json.dumps(
            {
                "candidates": [
                    {
                        "id": "malaria",
                        "note": "",
                        "score": 80,
                        "evidence": ["F4"],
                        "sources": [],
                    }
                ]
            }
        )
        return LLMReply(text=text, model=self.model, latency_ms=1)


@pytest.fixture
def fake_engine(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AIEngine:
    eng = AIEngine(
        AISettings(MODE="single", RPM_LIMIT=0, LOG_PATH=tmp_path / "log.jsonl"),
        OneShot(),
    )
    monkeypatch.setattr(ai_route, "get_ai_engine", lambda: eng)
    monkeypatch.setattr(triage_container, "get_ai_engine", lambda: eng)
    return eng


class Broken(OneShot):
    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        self.calls += 1
        raise LLMServerError("503")


def calls(eng: AIEngine) -> int:
    assert isinstance(eng.client, OneShot)
    return eng.client.calls


SCORE = f"{settings.API_V1_STR}/triage/flows/infection/score"


@pytest.mark.usefixtures("fake_engine")
def test_ai_endpoints_need_admin() -> None:
    with TestClient(app) as client:
        for path, body in (
            ("score", {"flow_id": "infection", "answers": MALARIA}),
            ("drugs", {"text": "bodrex"}),
        ):
            r = client.post(f"{settings.API_V1_STR}/ai/{path}", json=body)
            assert r.status_code == 401, (path, r.text)


@pytest.mark.usefixtures("fake_engine", "as_admin")
def test_ai_score_endpoint() -> None:
    with TestClient(app) as client:
        r = client.post(
            f"{settings.API_V1_STR}/ai/score",
            json={"flow_id": "infection", "answers": MALARIA},
        )
    assert r.status_code == 200, r.text
    body = r.json()
    assert (body["engine"], body["fallback"], body["reason"]) == ("ai", False, None)
    assert body["ranked"][0]["id"] == "malaria"
    assert body["ranked"][0]["reasons"] == [
        "Demam menggigil berulang teratur tiap 2–3 hari"
    ]
    assert body["scores"]["dbd"] == 0


@pytest.mark.usefixtures("fake_engine", "as_admin")
def test_ai_score_rejects_unknown_flow() -> None:
    with TestClient(app) as client:
        r = client.post(
            f"{settings.API_V1_STR}/ai/score", json={"flow_id": "x", "answers": {}}
        )
    assert r.status_code == 422


def test_engine_setting_ai(
    fake_engine: AIEngine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    assert triage_container.get_scoring_engine() is fake_engine
    with TestClient(app) as client:
        r = client.post(
            f"{settings.API_V1_STR}/triage/flows/infection/score", json=MALARIA
        )
    assert r.status_code == 200, r.text
    assert r.json()["top"]["id"] == "malaria"
    assert (r.json()["engine"], r.json()["fallback"]) == ("ai", False)


def test_score_result_says_fallback(
    fake_engine: AIEngine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    monkeypatch.setattr(fake_engine, "client", Broken())
    with TestClient(app) as client:
        r = client.post(SCORE, json=MALARIA)
    assert r.status_code == 200, r.text
    assert (r.json()["engine"], r.json()["fallback"]) == ("rules", True)
    assert r.json()["top"]["id"] == "malaria"


def test_preview_never_calls_the_model(
    fake_engine: AIEngine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    with TestClient(app) as client:
        r = client.post(f"{SCORE}?preview=true", json=MALARIA)
    assert r.status_code == 200, r.text
    assert (r.json()["engine"], r.json()["fallback"]) == ("rules", False)
    assert calls(fake_engine) == 0


def test_same_answers_call_the_model_once(
    fake_engine: AIEngine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    with TestClient(app) as client:
        first = client.post(SCORE, json=MALARIA).json()
        # Drugs and the finish time do not change the scores.
        again = {
            **MALARIA,
            "drugs": "",
            "taken_at": "2026-10-15T09:00:00+07:00",
        }
        second = client.post(SCORE, json=again).json()
        third = client.post(SCORE, json={**MALARIA, "age": 23}).json()
    assert calls(fake_engine) == 2
    assert first["engine"] == second["engine"] == third["engine"] == "ai"
    assert first["top"] == second["top"]


def test_fallback_is_not_cached(
    fake_engine: AIEngine, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    broken = Broken()
    monkeypatch.setattr(fake_engine, "client", broken)
    with TestClient(app) as client:
        assert client.post(SCORE, json=MALARIA).json()["fallback"] is True
        monkeypatch.setattr(fake_engine, "client", OneShot())
        assert client.post(SCORE, json=MALARIA).json()["engine"] == "ai"
    assert broken.calls == 2  # one retry after the 503
    assert calls(fake_engine) == 1


def test_cache_expires(fake_engine: AIEngine) -> None:
    content = get_content("infection")
    answers = Answers.model_validate(MALARIA)
    fake_engine.score(answers, content)
    hit = fake_engine.score(answers, content)
    assert hit.meta is not None and hit.meta.cached and hit.meta.calls == 0
    # Age the entry past the TTL: the next call goes to the model again.
    key = fake_engine._cache_key(answers, content)
    _, entry = fake_engine._cache[key]
    fake_engine._cache[key] = (-1e9, entry)
    fake_engine.score(answers, content)
    assert calls(fake_engine) == 2


def test_screening_saves_the_engine_used(
    fake_engine: AIEngine,
    monkeypatch: pytest.MonkeyPatch,
    db: Session,
    normal_user_token_headers: dict[str, str],
) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "ai")
    with TestClient(app) as client:
        shown = client.post(SCORE, json=MALARIA).json()
        r = client.post(
            f"{settings.API_V1_STR}/triage/screenings",
            headers=normal_user_token_headers,
            json={"flow_id": "infection", "answers": MALARIA, "consent": True},
        )
    assert r.status_code == 200, r.text
    assert r.json()["engine"] == "ai" and r.json()["top"] == shown["top"]
    # Saving reused the result the patient saw: one model call in total.
    assert calls(fake_engine) == 1
    row = db.exec(
        select(Screening).order_by(col(Screening.created_at).desc()).limit(1)
    ).one()
    assert row.engine == "ai"


@pytest.mark.usefixtures("as_admin")
def test_ai_drugs_endpoint(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from app.triage.ai.drugs import AIDrugRecognizer

    class DrugReply:
        model = "fake-model"

        def generate_json(
            self, system: str, user: str, schema: dict[str, Any], timeout: float
        ) -> LLMReply:
            text = '{"drugs": [{"mention": "bodrex", "generic": "ibuprofen", "class": "nsaid"}]}'
            return LLMReply(text=text, model=self.model, latency_ms=1)

    rec = AIDrugRecognizer(
        AISettings(API_KEY="k", RPM_LIMIT=0, LOG_PATH=tmp_path / "d.jsonl"), DrugReply()
    )
    monkeypatch.setattr(ai_route, "get_drug_recognizer", lambda: rec)
    with TestClient(app) as client:
        r = client.post(f"{settings.API_V1_STR}/ai/drugs", json={"text": "bodrex"})
    assert r.status_code == 200, r.text
    body = r.json()
    assert (body["engine"], body["classes"]) == ("ai", ["nsaid"])
    assert body["drugs"][0]["drug_class"] == "nsaid"
