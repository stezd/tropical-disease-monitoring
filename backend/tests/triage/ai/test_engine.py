import json
import re
import threading
import time
from pathlib import Path
from typing import Any

import pytest

from app.domain.answers import Answers
from app.triage.advice import build_result
from app.triage.ai import prompts
from app.triage.ai.call_log import CallLog
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine, shortlist
from app.triage.ai.llm import (
    LLMBadResponse,
    LLMReply,
    LLMServerError,
    LLMTimeout,
)
from app.triage.ai.llm import (
    LLMRateLimited as RateLimited,
)
from app.triage.ai.quota import QuotaGuard
from app.triage.content import FlowContent, get_content
from app.triage.scoring import RuleEngine

# Same case as docs/Format-MedGemma.md: malaria pattern, Papua, Paracetamol.
MALARIA = {
    "who": "self",
    "age": 22,
    "sex": "L",
    "red_flags": ["none"],
    "complaint": "A",
    "pattern": "malaria",
    "companion": ["malaria"],
    "eco": ["timur"],
    "province": "Papua",
    "drugs": "Paracetamol",
    "no_thermo": True,
    "vital_proxy": ["menggigil"],
    "nutrition_proxy": "longgar",
    "body": ["head"],
    "pain": 4,
    "findings": ["none"],
}


class FakeClient:
    """Scripted model. `reply(system, user, schema)` returns the JSON text or raises."""

    model = "fake-model"

    def __init__(self, reply: Any) -> None:
        self._reply = reply
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self._lock = threading.Lock()

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        assert timeout > 0
        with self._lock:
            self.calls.append((system, user, schema))
        text = self._reply(system, user, schema)
        return LLMReply(text=text, model=self.model, latency_ms=5, input_tokens=100)


def settings(**kw: Any) -> AISettings:
    base: dict[str, Any] = {
        "API_KEY": "test",
        "RPM_LIMIT": 0,
        "RPD_LIMIT": 0,
        "DEADLINE_S": 5,
        "CALL_TIMEOUT_S": 2,
        "LOG_PATH": None,
    }
    return AISettings(**{**base, **kw})


def engine(reply: Any, tmp_path: Path, **kw: Any) -> tuple[AIEngine, FakeClient]:
    client = FakeClient(reply)
    s = settings(LOG_PATH=tmp_path / "calls.jsonl", **kw)
    return AIEngine(s, client), client


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


@pytest.fixture
def answers() -> Answers:
    return Answers.model_validate(MALARIA)


def single_reply(_s: str, _u: str, _schema: dict[str, Any]) -> str:
    return json.dumps(
        {
            "candidates": [
                {
                    "id": "malaria",
                    "note": "Pola menggigil berkala + Papua.",
                    "score": 82,
                    "evidence": ["F4", "F5", "F6", "F99"],
                    "sources": ["S2", "S1"],
                },
                {"id": "covid", "note": "", "score": 90, "evidence": [], "sources": []},
                {
                    "id": "dbd",
                    "note": "",
                    "score": 20,
                    "evidence": ["F3"],
                    "sources": [],
                },
            ]
        }
    )


def candidate_of(user: str) -> str:
    m = re.search(r"^Kandidat: (\w+) ", user, re.MULTILINE)
    assert m
    return m.group(1)


def one_reply(_s: str, user: str, _schema: dict[str, Any]) -> str:
    score = {"malaria": 85, "dbd": 25, "chik": 10}.get(candidate_of(user), 5)
    return json.dumps(
        {"note": "ok", "score": score, "evidence": ["F4", "F6"], "sources": ["S1"]}
    )


# ── Single mode ────────────────────────────────────────────────────────────


def test_single_mode_scores_and_validates(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(single_reply, tmp_path, MODE="single")
    b = eng.score(answers, content)
    assert b.meta is not None
    assert (b.meta.engine, b.meta.fallback, b.meta.calls) == ("ai", False, 1)
    assert [r.id for r in b.ranked] == ["malaria", "dbd"]
    assert b.scores["malaria"] == 82 and b.scores["chik"] == 0
    # Unknown candidate, unknown fact ID, and a source about another disease
    # (S1 is the first candidate's, dbd) are dropped and counted.
    assert b.meta.invalid_ids == 3
    assert b.reasons["malaria"][0] == "Demam menggigil berulang teratur tiap 2–3 hari"
    assert b.meta.notes["malaria"] == "Pola menggigil berkala + Papua."
    [cited] = b.meta.sources["malaria"]
    assert "Malaria" in cited and "hlm." in cited

    system, user, schema = client.calls[0]
    assert system == prompts.SYSTEM_SINGLE
    # Drugs never reach the scoring prompt.
    assert "Paracetamol" not in user and "obat_pasien" not in user
    assert "F2 Provinsi tempat tinggal: Papua" in user
    # Every excerpt is labelled with a scored disease ID.
    labels = re.findall(r"^\[S\d+\] (\w+) · ", user, re.MULTILINE)
    assert labels and set(labels) <= set(content.scored_diseases)
    assert "Ditanyakan, tidak dipilih:" in user
    assert "- Pola gejala: Tinggi mendadak, turun hari ke-3/4, tapi makin lemas" in user
    item = schema["properties"]["candidates"]["items"]
    assert item["properties"]["id"]["enum"] == content.scored_diseases

    # The breakdown plugs into the normal result.
    result = build_result("infection", answers, content, b)
    assert result.top is not None and result.top.id == "malaria"


def test_single_mode_too_many_candidates_keeps_top_five(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    ids = content.scored_diseases[:8]

    def reply(_s: str, _u: str, _schema: dict[str, Any]) -> str:
        items = [
            {"id": d, "note": "", "score": 10 * i, "evidence": [], "sources": []}
            for i, d in enumerate(ids)
        ]
        return json.dumps({"candidates": items})

    eng, _ = engine(reply, tmp_path, MODE="single")
    b = eng.score(answers, content)
    assert b.meta is not None and b.meta.engine == "ai"
    assert [r.id for r in b.ranked] == ids[7:2:-1]


# ── Per-candidate mode ─────────────────────────────────────────────────────


def test_shortlist_is_cluster_plus_rule_top(
    content: FlowContent, answers: Answers
) -> None:
    rules = RuleEngine().score(answers, content)
    short = shortlist(answers, content, rules, 2)
    assert short[:5] == ["dbd", "malaria", "chik", "lepto", "skisto"]
    assert len(short) == len(set(short))
    other = Answers.model_validate({**MALARIA, "complaint": "B", "pattern": "tbc"})
    rules = RuleEngine().score(other, content)
    short = shortlist(other, content, rules, 2)
    assert short[:2] == ["ispa", "tbc"] and "malaria" in short


def test_per_candidate_one_call_each(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(one_reply, tmp_path, MODE="per_candidate")
    b = eng.score(answers, content)
    assert b.meta is not None
    assert b.meta.engine == "ai" and not b.meta.fallback
    assert b.meta.calls == len(b.meta.shortlist) == len(client.calls) == 5
    assert [r.id for r in b.ranked][:3] == ["malaria", "dbd", "chik"]
    assert b.meta.sources["malaria"]
    for system, user, schema in client.calls:
        assert system == prompts.SYSTEM_ONE
        cand = candidate_of(user)
        assert "Paracetamol" not in user
        # Literature only about this candidate.
        assert set(re.findall(r"^\[S\d+\] (\w+) · ", user, re.MULTILINE)) <= {cand}
        assert "id" not in schema["properties"]
    dbd_user = next(u for _, u, _ in client.calls if candidate_of(u) == "dbd")
    assert (
        "- Pola gejala: Tinggi mendadak, turun hari ke-3/4, tapi makin lemas"
        in dbd_user
    )
    assert "- Gejala penyerta: Nyeri belakang mata / sakit kepala hebat" in dbd_user
    result = build_result("infection", answers, content, b)
    assert result.top is not None and result.top.id == "malaria"


def test_asked_not_picked_other_cluster(content: FlowContent) -> None:
    a = Answers.model_validate(
        {
            "age": 30,
            "complaint": "C",
            "pattern": "diare",
            "eco": ["none"],
            "body": ["low"],
        }
    )
    malaria = prompts.asked_not_picked(a, content, "malaria")
    assert "Keluhan utama: Demam & Badan" in malaria
    # Eco answered "none": every eco option for malaria counts as not picked.
    assert (
        "Riwayat / faktor risiko: Dari Papua/Maluku/NTT, hutan, atau tambang" in malaria
    )
    lepto = prompts.asked_not_picked(a, content, "lepto")
    assert "Nyeri: Betis kanan, Betis kiri" in lepto
    amoeba = prompts.asked_not_picked(a, content, "amoeba")
    assert "Pola gejala: BAB berdarah & berlendir, perih saat mengejan" in amoeba
    # Not answered: nothing claimed absent.
    assert not prompts.asked_not_picked(Answers(age=30), content, "malaria")


# ── Fallbacks ──────────────────────────────────────────────────────────────


def rules_scores(answers: Answers, content: FlowContent) -> dict[str, float]:
    return RuleEngine().score(answers, content).scores


def raising(exc: Exception) -> Any:
    def reply(_s: str, _u: str, _schema: dict[str, Any]) -> str:
        raise exc

    return reply


@pytest.mark.parametrize("mode", ["single", "per_candidate"])
@pytest.mark.parametrize(
    ("reply", "reason"),
    [
        (raising(LLMTimeout("slow")), "timeout"),
        (raising(RateLimited("429")), "rate_limited"),
        (raising(LLMBadResponse("blocked")), "bad_response"),
        (lambda *_: "not json", "bad_response"),
        (lambda *_: '{"candidates": [{"id": "dbd", "score": 150}]}', "bad_response"),
        (lambda *_: '{"score": "high"}', "bad_response"),
        (raising(RuntimeError("bug")), "error"),
    ],
)
def test_fallback_to_rules(
    content: FlowContent,
    answers: Answers,
    tmp_path: Path,
    mode: str,
    reply: Any,
    reason: str,
) -> None:
    eng, _ = engine(reply, tmp_path, MODE=mode)
    b = eng.score(answers, content)
    assert b.meta is not None
    assert (b.meta.engine, b.meta.fallback, b.meta.reason) == ("rules", True, reason)
    assert b.scores == rules_scores(answers, content)


def test_model_off_is_flagged(content: FlowContent, answers: Answers) -> None:
    eng = AIEngine(settings(), None)
    b = eng.score(answers, content)
    assert b.meta is not None
    assert (b.meta.engine, b.meta.fallback, b.meta.reason) == (
        "rules",
        True,
        "model_off",
    )


def test_red_flag_skips_model(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(single_reply, tmp_path)
    red = answers.model_copy(update={"red_flags": ["syok"]})
    b = eng.score(red, content)
    assert b.meta is not None and not client.calls
    assert (b.meta.engine, b.meta.fallback) == ("rules", False)
    assert b.meta.reason == "skipped:red_flag_or_empty"


def test_local_quota_falls_back_without_calling(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(one_reply, tmp_path, MODE="per_candidate", RPM_LIMIT=3)
    b = eng.score(answers, content)
    assert b.meta is not None and b.meta.reason == "quota_local"
    assert not client.calls


def test_429_starts_cooldown(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(raising(RateLimited("429")), tmp_path, RPM_LIMIT=100)
    assert eng.score(answers, content).meta.reason == "rate_limited"  # type: ignore[union-attr]
    assert eng.score(answers, content).meta.reason == "quota_local"  # type: ignore[union-attr]
    assert len(client.calls) == 1


def test_server_error_is_retried_once(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    attempts = {"n": 0}

    def flaky(s: str, u: str, schema: dict[str, Any]) -> str:
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise LLMServerError("503")
        return single_reply(s, u, schema)

    eng, _ = engine(flaky, tmp_path, MODE="single")
    b = eng.score(answers, content)
    assert b.meta is not None and b.meta.engine == "ai" and b.meta.calls == 2


def test_deadline_in_parallel_mode(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    def slow(s: str, u: str, schema: dict[str, Any]) -> str:
        if candidate_of(u) == "lepto":
            time.sleep(2.5)
        return one_reply(s, u, schema)

    eng, _ = engine(slow, tmp_path, MODE="per_candidate", DEADLINE_S=1.2)
    start = time.monotonic()
    b = eng.score(answers, content)
    assert time.monotonic() - start < 2.0
    assert b.meta is not None and b.meta.reason == "timeout"


# ── Log ────────────────────────────────────────────────────────────────────


def test_call_log_has_no_free_text(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, _ = engine(single_reply, tmp_path, MODE="single")
    eng.score(
        answers.model_copy(update={"drugs": "Budi Santoso, Paracetamol"}), content
    )
    lines = (tmp_path / "calls.jsonl").read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[-1])
    assert rec["engine"] == "ai" and rec["model"] == "fake-model"
    assert rec["scores"][0] == ["malaria", 82.0]
    assert rec["rules"][0][0] == "malaria"
    assert "F2 Provinsi tempat tinggal: Papua" in rec["facts"]
    assert "Budi" not in lines[-1] and "Paracetamol" not in lines[-1]


def test_call_log_never_raises(tmp_path: Path) -> None:
    blocked = tmp_path / "file"
    blocked.write_text("x")
    CallLog(blocked / "calls.jsonl").write({"a": 1})


def test_quota_guard_window() -> None:
    now = {"t": 0.0}
    q = QuotaGuard(rpm=3, rpd=4, cooldown_s=10, clock=lambda: now["t"])
    assert q.try_acquire(2) and not q.try_acquire(2) and q.try_acquire(1)
    now["t"] = 61
    assert q.try_acquire(1) and not q.try_acquire(1)  # daily limit 4
    q2 = QuotaGuard(rpm=0, clock=lambda: now["t"])
    q2.note_rate_limited()
    assert not q2.try_acquire()
    now["t"] += 61
    assert q2.try_acquire()


# ── Engine label and reuse ─────────────────────────────────────────────────


def test_same_answers_reuse_model_result(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(single_reply, tmp_path, MODE="single")
    first = eng.score(answers, content)
    again = eng.score(answers.model_copy(update={"taken_at": None}), content)
    assert len(client.calls) == 1
    assert first.engine == again.engine == "ai"
    assert again.meta is not None and again.meta.cached and again.meta.calls == 0
    assert again.scores == first.scores
    # Different answers: a new call.
    eng.score(answers.model_copy(update={"province": "Maluku"}), content)
    assert len(client.calls) == 2


def test_fallbacks_are_not_reused(
    content: FlowContent, answers: Answers, tmp_path: Path
) -> None:
    eng, client = engine(raising(LLMTimeout("slow")), tmp_path, MODE="single")
    b = eng.score(answers, content)
    assert b.engine == "ai-fb:timeout"
    eng.score(answers, content)
    assert len(client.calls) == 2


def test_engine_labels(content: FlowContent, answers: Answers, tmp_path: Path) -> None:
    assert (
        AIEngine(settings(), None).score(answers, content).engine == "ai-fb:model_off"
    )
    eng, _ = engine(raising(RateLimited("429")), tmp_path, MODE="single")
    assert eng.score(answers, content).engine == "ai-fb:rate_limited"
    red = answers.model_copy(update={"red_flags": ["syok"]})
    assert eng.score(red, content).engine == "rules"
    assert all(len(x) <= 20 for x in ("ai-fb:rate_limited", "ai-fb:bad_response"))
