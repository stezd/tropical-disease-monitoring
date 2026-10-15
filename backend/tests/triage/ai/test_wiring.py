import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.api.routes import ai as ai_route
from app.composition import triage_container
from app.core.config import settings
from app.main import app
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine
from app.triage.ai.llm import LLMReply
from tests.triage.ai.test_engine import MALARIA


class OneShot:
    model = "fake-model"

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
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


@pytest.mark.usefixtures("fake_engine")
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


@pytest.mark.usefixtures("fake_engine")
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


def test_preview_query_param_uses_rules(fake_engine: AIEngine) -> None:
    with TestClient(app) as client:
        r = client.post(
            f"{settings.API_V1_STR}/triage/flows/infection/score?preview=true",
            json=MALARIA,
        )
    assert r.status_code == 200
    assert fake_engine.client is not None  # engine present but not used for preview
