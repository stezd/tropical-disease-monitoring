import json
import threading
from pathlib import Path
from typing import Any

import pytest

from app.application.use_cases.score_flow import ScoreFlowUseCase
from app.domain.answers import Answers
from app.domain.warnings import drug_classes_wanted, drug_flags
from app.triage.ai.config import AISettings
from app.triage.ai.drugs import AIDrugRecognizer, items, needs_model
from app.triage.ai.engine import AIEngine
from app.triage.ai.llm import LLMReply, LLMTimeout
from app.triage.content import FlowContent, get_content
from app.triage.scoring import RuleEngine
from tests.triage.ai.test_engine import MALARIA, single_reply
from tests.triage.test_composition import FakeContentRepository

FEVER = {"age": 30, "complaint": "A", "pattern": "dbd", "temp": 38.5}


class Scripted:
    model = "fake-model"

    def __init__(self, reply: Any) -> None:
        self._reply = reply
        self.calls: list[str] = []
        self._lock = threading.Lock()

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        with self._lock:
            self.calls.append(user)
        if isinstance(self._reply, Exception):
            raise self._reply
        return LLMReply(text=self._reply, model=self.model, latency_ms=3)


def reply(*drugs: tuple[str, str, str]) -> str:
    return json.dumps(
        {"drugs": [{"mention": m, "generic": g, "class": c} for m, g, c in drugs]}
    )


def recognizer(
    answer: Any, tmp_path: Path, **kw: Any
) -> tuple[AIDrugRecognizer, Scripted]:
    client = Scripted(answer)
    s = AISettings(API_KEY="k", RPM_LIMIT=0, LOG_PATH=tmp_path / "log.jsonl", **kw)
    return AIDrugRecognizer(s, client), client


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


def test_items_split() -> None:
    assert items("Paracetamol, ibu profen dan oralit") == [
        "paracetamol",
        "ibu profen",
        "oralit",
    ]
    assert items("bodrex+  neozep / CTM") == ["bodrex", "neozep", "ctm"]


def test_known_drugs_need_no_model() -> None:
    # Drug chips and advice.json keywords are handled without a call.
    assert not needs_model("Paracetamol, Oralit", "infection")
    assert not needs_model("ibuprofen 400", "infection")
    assert needs_model("Paracetamol, bodrex migra", "infection")


def test_class_fires_existing_rule(content: FlowContent) -> None:
    a = Answers.model_validate({**FEVER, "drugs": "bodrex migra"})
    assert drug_flags(a, content) == []
    assert drug_flags(a, content, frozenset({"nsaid"})) == ["nsaid"]
    # The rule's conditions still apply: NSAID only for fever (complaint A).
    skin = a.model_copy(update={"complaint": "D", "pattern": "scabies"})
    assert drug_flags(skin, content, frozenset({"nsaid"})) == []


def test_pending_dr_rules_never_fire(content: FlowContent) -> None:
    a = Answers.model_validate({**FEVER, "drugs": "warfarin, simvastatin"})
    assert drug_flags(a, content, frozenset({"antikoagulan", "statin"})) == []
    assert content.advice.drugs["anticoagulant_dengue"].pending_dr


def test_classes_wanted(content: FlowContent) -> None:
    fever = Answers.model_validate({**FEVER, "drugs": "bodrex"})
    assert "nsaid" in drug_classes_wanted(fever, content)
    # Keyword already caught the NSAID: no need to ask the model for it.
    ibu = fever.model_copy(update={"drugs": "ibuprofen"})
    assert "nsaid" not in drug_classes_wanted(ibu, content)
    # Skin complaint: no rule can fire, so nothing is wanted.
    skin = Answers.model_validate(
        {"complaint": "D", "pattern": "scabies", "drugs": "x"}
    )
    assert drug_classes_wanted(skin, content) == frozenset()
    # Pending rules are never wanted.
    assert "statin" not in drug_classes_wanted(fever, content)


def test_recognizer_returns_actionable_classes(tmp_path: Path) -> None:
    r, client = recognizer(
        reply(
            ("bodrex migra", "ibuprofen + paracetamol", "nsaid"),
            ("neozep", "phenylephrine + paracetamol", "lain"),
        ),
        tmp_path,
    )
    out = r.recognize("Bodrex migra, neozep", "infection")
    assert (out.engine, out.fallback, out.classes) == ("ai", False, ["nsaid"])
    assert len(out.drugs) == 2
    assert client.calls == ["<obat_pasien>Bodrex migra, neozep</obat_pasien>"]
    # Same text again: cached, no second call.
    assert r.classes("bodrex migra , neozep", "infection") == frozenset({"nsaid"})
    assert len(client.calls) == 1


def test_recognizer_skips_model_for_known_drugs(tmp_path: Path) -> None:
    r, client = recognizer(reply(), tmp_path)
    assert r.recognize("Paracetamol", "infection").engine == "keywords"
    assert r.recognize("  ", "infection").engine == "none"
    assert not client.calls


@pytest.mark.parametrize(
    ("answer", "reason"),
    [
        (LLMTimeout("slow"), "timeout"),
        ("not json", "bad_response"),
        (
            '{"drugs": [{"mention": "x", "generic": "x", "class": "opioid"}]}',
            "bad_response",
        ),
        ('{"nothing": 1}', "bad_response"),
    ],
)
def test_recognizer_fallback(answer: Any, reason: str, tmp_path: Path) -> None:
    r, _ = recognizer(answer, tmp_path)
    out = r.recognize("obat warung", "infection")
    assert (out.fallback, out.reason, out.classes) == (True, reason, [])


def test_recognizer_log_keeps_patient_wording_out(tmp_path: Path) -> None:
    r, _ = recognizer(reply(("obat dari Bu Sari", "ibuprofen", "nsaid")), tmp_path)
    r.recognize("obat dari Bu Sari", "infection")
    line = (tmp_path / "log.jsonl").read_text(encoding="utf-8")
    assert "Sari" not in line and '"ibuprofen"' in line


# ── Use case ───────────────────────────────────────────────────────────────


class FakeDrugs:
    def __init__(self, classes: frozenset[str]) -> None:
        self.calls: list[str] = []
        self._classes = classes

    def classes(self, text: str, flow_id: str) -> frozenset[str]:
        self.calls.append(text)
        return self._classes


def use_case(engine: Any, drugs: Any) -> ScoreFlowUseCase:
    return ScoreFlowUseCase(
        FakeContentRepository(get_content("infection")),
        engine,
        preview_engine=RuleEngine(),
        drugs=drugs,
    )


def test_use_case_adds_drug_popup_from_class() -> None:
    drugs = FakeDrugs(frozenset({"nsaid"}))
    a = Answers.model_validate({**FEVER, "drugs": "bodrex migra"})
    scored = use_case(RuleEngine(), drugs).execute_detailed("infection", a)
    assert drugs.calls == ["bodrex migra"]
    assert scored.drug_classes == frozenset({"nsaid"})
    assert [p.level for p in scored.result.drug_popups] == ["r"]
    assert scored.engine == "rules"


def test_use_case_skips_recognizer_when_no_rule_can_fire() -> None:
    drugs = FakeDrugs(frozenset({"nsaid"}))
    a = Answers.model_validate({**FEVER, "drugs": "ibuprofen"})  # keyword already
    use_case(RuleEngine(), drugs).execute("infection", a)
    assert drugs.calls == []


def test_preview_never_uses_the_model(tmp_path: Path) -> None:
    from tests.triage.ai.test_engine import FakeClient

    client = FakeClient(single_reply)
    ai = AIEngine(
        AISettings(API_KEY="k", RPM_LIMIT=0, MODE="single", LOG_PATH=tmp_path / "l"),
        client,
    )
    uc = use_case(ai, None)
    a = Answers.model_validate(MALARIA)
    preview = uc.execute_detailed("infection", a, preview=True)
    assert preview.engine == "rules" and not client.calls
    final = uc.execute_detailed("infection", a)
    assert final.engine == "ai" and len(client.calls) == 1
