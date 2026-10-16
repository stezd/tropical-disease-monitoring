"""AIEngine: a ScoringEngine backed by a language model, with RuleEngine as fallback.

    answers ─► build_request() ─► facts F1..Fn (no drugs, no identity)
            ─► literature per candidate (pre-computed, labelled with the disease ID)
            ─► mode "single":        one call, all candidates
               mode "per_candidate": one call per shortlisted candidate, in parallel
            ─► validate (schema + known IDs only) ─► to_breakdown() ─► AIBreakdown

Anything that goes wrong (no key, local quota, 429, timeout, bad JSON) returns
RuleEngine's breakdown with `meta.fallback = True` and the reason. Red flags never reach
the model (build_request returns None) and are not a fallback.

Successful AI results are kept in memory for CACHE_TTL_S (keyed by flow and answers,
without drugs and time), so the same answers scored again (saving the screening, the
QR page) give the same result without a new model call.
"""

import logging
import threading
import time
import uuid
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures import TimeoutError as FuturesTimeout
from dataclasses import asdict, dataclass, field, replace
from datetime import UTC, datetime
from functools import cache
from typing import Any, Literal

from pydantic import ValidationError

from app.domain.answers import Answers
from app.triage.ai import prompts
from app.triage.ai.call_log import CallLog
from app.triage.ai.config import AISettings
from app.triage.ai.literature import (
    Chunk,
    Literature,
    answer_keys,
    as_sources,
    get_literature,
)
from app.triage.ai.llm import (
    LLMBadResponse,
    LLMClient,
    LLMError,
    LLMRateLimited,
    LLMReply,
    LLMTimeout,
    json_object,
    make_client,
)
from app.triage.ai.quota import QuotaGuard, shared_quota
from app.triage.content import FlowContent
from app.triage.Gemma4 import (
    MAX_CANDIDATES,
    ScoredCandidate,
    TextOutput,
    TextRequest,
    build_request,
    to_breakdown,
)
from app.triage.scoring import RuleEngine, ScoreBreakdown, ScoringEngine

logger = logging.getLogger("app.triage.ai")


class QuotaExhausted(LLMError):
    kind = "quota_local"


@dataclass
class AIMeta:
    request_id: str
    # What produced the scores. "rules" with fallback=False = the model was not needed
    # (red flag, nothing to score).
    engine: Literal["ai", "rules"]
    fallback: bool
    reason: str | None
    mode: str
    model: str
    prompt_version: str
    latency_ms: int
    calls: int = 0
    shortlist: list[str] = field(default_factory=list)
    # Disease ID → citations of the excerpts the model said it used.
    sources: dict[str, list[str]] = field(default_factory=dict)
    # Disease ID → the model's one-line note. For the review team, not for patients.
    notes: dict[str, str] = field(default_factory=dict)
    # IDs the model returned that were not offered (dropped). Should stay 0.
    invalid_ids: int = 0
    # True = same answers scored a moment ago (e.g. result page, then saving the
    # screening): the earlier model result was reused, no new call.
    cached: bool = False

    def label(self) -> str:
        """Short engine label for the screening table (max 20 characters)."""
        if self.engine == "ai":
            return "ai"
        return f"ai-fb:{self.reason}"[:20] if self.fallback else "rules"


@dataclass
class AIBreakdown(ScoreBreakdown):
    meta: AIMeta | None = None


@dataclass
class _Run:
    """Counters for one scoring, shared by parallel calls."""

    deadline: float
    calls: int = 0
    tokens_in: int = 0
    tokens_out: int = 0
    lock: threading.Lock = field(default_factory=threading.Lock)

    def add(self, r: LLMReply) -> None:
        with self.lock:
            self.tokens_in += r.input_tokens or 0
            self.tokens_out += r.output_tokens or 0

    def count(self) -> None:
        with self.lock:
            self.calls += 1


@dataclass
class _Scored:
    score: int
    evidence: list[str]
    chunks: list[Chunk]
    note: str


def shortlist(
    a: Answers, content: FlowContent, rules: ScoreBreakdown, rule_top: int
) -> list[str]:
    """Members of the chosen cluster, then RuleEngine's top scores. No duplicates."""
    scored = set(content.scored_diseases)
    cluster = next((c for c in content.flow.clusters if c.id == a.complaint), None)
    ids = [m for m in cluster.members if m in scored] if cluster else []
    ids += [r.id for r in rules.ranked[:rule_top]]
    return list(dict.fromkeys(ids))


# Tolerant JSON extraction lives with the clients: see llm.json_object.
_json_object = json_object


# Facts sent to the model but never shown to the patient as a reason ("Kenapa aku
# menebak ini?"): age and sex are context, not evidence for a disease.
HIDDEN_REASON_LABELS = frozenset({"Pasien"})


def _without_patient_line(out: TextOutput, req: TextRequest) -> TextOutput:
    hidden = {f.id for f in req.facts if f.label in HIDDEN_REASON_LABELS}
    return TextOutput(
        candidates=[
            c.model_copy(
                update={"evidence": [e for e in c.evidence if e not in hidden]}
            )
            for c in out.candidates
        ]
    )


def _note(raw: Any) -> str:
    return " ".join(str(raw or "").split())[:200]


class AIEngine:
    def __init__(
        self,
        settings: AISettings,
        client: LLMClient | None,
        quota: QuotaGuard | None = None,
        log: CallLog | None = None,
        rules: ScoringEngine | None = None,
    ) -> None:
        self.s = settings
        self.client = client
        self.quota = quota or QuotaGuard(
            settings.RPM_LIMIT, settings.RPD_LIMIT, settings.COOLDOWN_S
        )
        self.log = log or CallLog(settings.LOG_PATH)
        self.rules = rules or RuleEngine()
        # (flow, answers) → model result, for CACHE_TTL_S. Only model results, never
        # fallbacks, so a retry after a failure gets a real attempt.
        self._cache: OrderedDict[str, tuple[float, AIBreakdown]] = OrderedDict()
        self._cache_lock = threading.Lock()

    def _cache_key(self, answers: Answers, content: FlowContent) -> str:
        # Drugs and time are not used for scoring, so they must not force a new call.
        ignored = {"taken_at", "drugs"}
        return f"{content.flow.id}|{answers.model_dump_json(exclude=ignored)}"

    def _cached(self, key: str) -> AIBreakdown | None:
        with self._cache_lock:
            hit = self._cache.get(key)
            if hit is None:
                return None
            at, b = hit
            if time.monotonic() - at > self.s.CACHE_TTL_S:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return b

    def _remember(self, key: str, b: AIBreakdown) -> None:
        if self.s.CACHE_TTL_S <= 0:
            return
        with self._cache_lock:
            self._cache[key] = (time.monotonic(), b)
            while len(self._cache) > 2048:
                self._cache.popitem(last=False)

    @property
    def model(self) -> str:
        return self.client.model if self.client else "-"

    def literature(self, flow_id: str) -> Literature:
        try:
            return get_literature(self.s.LITERATURE_DIR, flow_id)
        except OSError, ValueError, KeyError:
            logger.exception("literature for %s could not be loaded", flow_id)
            return Literature(None)

    # ── ScoringEngine ──────────────────────────────────────────────────────

    def score(self, answers: Answers, content: FlowContent) -> AIBreakdown:
        key = self._cache_key(answers, content)
        if (hit := self._cached(key)) is not None and hit.meta is not None:
            meta = replace(hit.meta, cached=True, calls=0, latency_ms=0)
            return replace(hit, meta=meta)
        start = time.monotonic()
        run = _Run(deadline=start + self.s.DEADLINE_S)
        rid = uuid.uuid4().hex[:12]
        rule_b = self.rules.score(answers, content)
        meta = AIMeta(
            request_id=rid,
            engine="rules",
            fallback=False,
            reason=None,
            mode=self.s.MODE,
            model=self.model,
            prompt_version=prompts.PROMPT_VERSION,
            latency_ms=0,
        )
        req = build_request(answers, content)
        result: ScoreBreakdown = rule_b
        if req is None:
            meta.reason = "skipped:red_flag_or_empty"
        elif content.flow.id not in self.s.flows():
            meta.reason = "skipped:flow_off"
        elif self.client is None:
            meta.fallback, meta.reason = True, "model_off"
        else:
            req = req.model_copy(update={"drugs": ""})
            try:
                if self.s.MODE == "single":
                    result = self._single(run, req, answers, content, meta)
                else:
                    short = shortlist(
                        answers, content, rule_b, self.s.SHORTLIST_RULE_TOP
                    )
                    meta.shortlist = short
                    if short:
                        result = self._per_candidate(
                            run, req, answers, content, short, meta
                        )
                    else:
                        meta.reason = "skipped:empty_shortlist"
                if result is not rule_b:
                    meta.engine = "ai"
            except LLMError as e:
                if isinstance(e, LLMRateLimited):
                    self.quota.note_rate_limited()
                meta.fallback, meta.reason = True, e.kind
                logger.warning("AI scoring fell back to rules (%s): %s", e.kind, e)
                result = rule_b
            except Exception:  # noqa: BLE001 - patients must always get a result
                logger.exception("AI scoring failed")
                meta.fallback, meta.reason = True, "error"
                result = rule_b
        meta.calls = run.calls
        meta.latency_ms = int((time.monotonic() - start) * 1000)
        self._write_log(content, req, rule_b, result, meta, run)
        out = AIBreakdown(
            scores=result.scores,
            reasons=result.reasons,
            ranked=result.ranked,
            engine=meta.label(),
            fallback=meta.fallback,
            meta=meta,
        )
        if meta.engine == "ai":
            # Only real model results: a fallback must not hide a later recovery.
            self._remember(key, out)
        return out

    # ── Calls ──────────────────────────────────────────────────────────────

    def _call(
        self, run: _Run, system: str, user: str, schema: dict[str, Any]
    ) -> LLMReply:
        assert self.client is not None
        attempt = 0
        while True:
            left = run.deadline - time.monotonic()
            if left < 1.0:
                raise LLMTimeout("deadline reached")
            run.count()
            try:
                reply = self.client.generate_json(
                    system, user, schema, min(self.s.CALL_TIMEOUT_S, left)
                )
                run.add(reply)
                return reply
            except LLMError as e:
                if not e.retryable or attempt >= self.s.RETRIES:
                    raise
                if not self.quota.try_acquire(1):
                    raise QuotaExhausted("no quota left for a retry") from e
                attempt += 1

    def _single(
        self,
        run: _Run,
        req: TextRequest,
        answers: Answers,
        content: FlowContent,
        meta: AIMeta,
    ) -> ScoreBreakdown:
        lit = self.literature(content.flow.id)
        keys = answer_keys(answers, content)
        chunks = list(
            dict.fromkeys(
                c
                for cand in req.candidates
                for c in lit.for_disease(
                    cand.id, keys, self.s.SOURCES_PER_CANDIDATE_SINGLE
                )
            )
        )
        sources = as_sources(chunks)
        by_sid = {s.id: c for s, c in zip(sources, chunks, strict=True)}
        req = req.model_copy(update={"sources": sources})
        absent = prompts.asked_not_picked(answers, content)
        if not self.quota.try_acquire(1):
            raise QuotaExhausted("local per-minute or per-day limit")
        reply = self._call(
            run,
            prompts.SYSTEM_SINGLE,
            prompts.single_message(req, absent),
            prompts.single_schema(req, MAX_CANDIDATES),
        )
        data = _json_object(reply.text)
        raw = data.get("candidates")
        if not isinstance(raw, list):
            raise LLMBadResponse("no candidates list")
        known = {c.id for c in req.candidates}
        facts = {f.id for f in req.facts}
        kept: dict[str, ScoredCandidate] = {}
        for item in raw:
            if isinstance(item, dict) and "id" not in item and "candidate" in item:
                # The judge names the field after the schema's "candidates" list.
                item = {**item, "id": item["candidate"]}
            try:
                c = ScoredCandidate.model_validate(item)
            except ValidationError as e:
                raise LLMBadResponse(f"bad candidate: {e.errors()[0]['msg']}") from e
            # A source counts only for the disease it is about.
            own = [s for s in c.sources if s in by_sid and by_sid[s].disease == c.id]
            bad = (c.id not in known) + sum(e not in facts for e in c.evidence)
            bad += len(c.sources) - len(own)
            meta.invalid_ids += bad
            if c.id in known and c.id not in kept:
                kept[c.id] = c.model_copy(update={"sources": own})
                if isinstance(item, dict) and (n := _note(item.get("note"))):
                    meta.notes[c.id] = n
        top = sorted(kept.values(), key=lambda c: c.score, reverse=True)[
            :MAX_CANDIDATES
        ]
        out = _without_patient_line(TextOutput(candidates=top).restrict_to(req), req)
        for c in out.candidates:
            if c.sources:
                meta.sources[c.id] = [by_sid[s].citation for s in c.sources]
        return to_breakdown(out, req, content)

    def _one(
        self,
        run: _Run,
        req: TextRequest,
        answers: Answers,
        content: FlowContent,
        lit: Literature,
        keys: list[str],
        disease: str,
    ) -> _Scored:
        chunks = lit.for_disease(disease, keys, self.s.SOURCES_PER_CANDIDATE)
        sources = as_sources(chunks)
        name = content.diseases[disease].name
        user = prompts.one_message(
            req.flow_id,
            disease,
            name,
            req.facts,
            prompts.asked_not_picked(answers, content, disease),
            sources,
        )
        reply = self._call(
            run, prompts.SYSTEM_ONE, user, prompts.one_schema(req.facts, sources)
        )
        data = _json_object(reply.text)
        try:
            c = ScoredCandidate.model_validate({**data, "id": disease})
        except ValidationError as e:
            raise LLMBadResponse(f"{disease}: {e.errors()[0]['msg']}") from e
        facts = {f.id for f in req.facts}
        by_sid = {s.id: ch for s, ch in zip(sources, chunks, strict=True)}
        return _Scored(
            score=c.score,
            evidence=list(dict.fromkeys(e for e in c.evidence if e in facts)),
            chunks=[by_sid[s] for s in dict.fromkeys(c.sources) if s in by_sid],
            note=_note(data.get("note")),
        )

    def _per_candidate(
        self,
        run: _Run,
        req: TextRequest,
        answers: Answers,
        content: FlowContent,
        short: list[str],
        meta: AIMeta,
    ) -> ScoreBreakdown:
        if not self.quota.try_acquire(len(short)):
            raise QuotaExhausted(f"local limit: {len(short)} calls needed")
        lit = self.literature(content.flow.id)
        keys = answer_keys(answers, content)
        results: dict[str, _Scored] = {}
        pool = ThreadPoolExecutor(
            max_workers=min(self.s.MAX_PARALLEL, len(short)),
            thread_name_prefix="ai-score",
        )
        try:
            futures = {
                pool.submit(self._one, run, req, answers, content, lit, keys, d): d
                for d in short
            }
            wait = max(0.1, run.deadline - time.monotonic())
            for f in as_completed(futures, timeout=wait):
                results[futures[f]] = f.result()
        except FuturesTimeout as e:
            raise LLMTimeout("deadline reached") from e
        finally:
            pool.shutdown(wait=False, cancel_futures=True)

        ranked = sorted(short, key=lambda d: results[d].score, reverse=True)
        top = [
            ScoredCandidate(id=d, score=results[d].score, evidence=results[d].evidence)
            for d in ranked[:MAX_CANDIDATES]
        ]
        for d in short:
            r = results[d]
            if r.note:
                meta.notes[d] = r.note
            if r.chunks:
                meta.sources[d] = [c.citation for c in r.chunks]
        req = req.model_copy(update={"sources": []})
        out = _without_patient_line(TextOutput(candidates=top), req)
        return to_breakdown(out, req, content)

    # ── Log ────────────────────────────────────────────────────────────────

    def _write_log(
        self,
        content: FlowContent,
        req: TextRequest | None,
        rule_b: ScoreBreakdown,
        result: ScoreBreakdown,
        meta: AIMeta,
        run: _Run,
    ) -> None:
        record: dict[str, Any] = {
            "ts": datetime.now(UTC).isoformat(timespec="seconds"),
            "flow_id": content.flow.id,
            **asdict(meta),
            "literature": self.literature(content.flow.id).version,
            "tokens_in": run.tokens_in,
            "tokens_out": run.tokens_out,
            "scores": [[r.id, r.score] for r in result.ranked[:MAX_CANDIDATES]],
            "rules": [[r.id, r.score] for r in rule_b.ranked[:MAX_CANDIDATES]],
        }
        if self.s.LOG_FACTS and req is not None:
            record["facts"] = [f"{f.id} {f.label}: {f.text}" for f in req.facts]
        self.log.write(record)

    def status(self) -> dict[str, Any]:
        """Health info for the ops endpoint. No secrets."""
        return {
            "provider": self.s.PROVIDER,
            "model": self.model,
            "enabled": self.client is not None,
            "mode": self.s.MODE,
            "prompt_version": prompts.PROMPT_VERSION,
            "quota": self.quota.snapshot(),
            "rpm_limit": self.s.RPM_LIMIT,
            "rpd_limit": self.s.RPD_LIMIT,
            "cache_entries": len(self._cache),
        }


@cache
def get_ai_engine() -> AIEngine:
    """One engine per process, so the quota guard sees every request."""
    s = AISettings()
    quota = shared_quota(s.RPM_LIMIT, s.RPD_LIMIT, s.COOLDOWN_S)
    return AIEngine(s, make_client(s), quota=quota)
