"""HTTP wrapper around app.triage.ai, for checking the model (superusers only: every
call spends the shared model quota).

The patient-facing result still comes from POST /triage/flows/{flow_id}/score; with
TRIAGE_SCORING_ENGINE=ai that endpoint uses the same engine.
"""

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.api.deps import get_current_active_superuser
from app.composition.triage_container import get_content_repository
from app.triage.ai import get_ai_engine
from app.triage.ai.drugs import DrugResult, get_drug_recognizer
from app.triage.schemas import Answers

router = APIRouter(prefix="/ai", tags=["ai"])


class AIScoreRequest(BaseModel):
    flow_id: Literal["infection", "chronic"]
    answers: Answers


class AIScoredDisease(BaseModel):
    id: str
    score: float
    # Softmax share over diseases with a positive score (0–1), as in ScoreBreakdown.
    share: float
    reasons: list[str]
    sources: list[str]


class AIScoreResponse(BaseModel):
    request_id: str
    # "ai" = scores from the model. "rules" = RuleEngine (fallback or not needed).
    engine: Literal["ai", "rules"]
    fallback: bool
    # Why the model was not used: model_off, quota_local, rate_limited, timeout,
    # bad_response, network, server_error, error, skipped:*. None when engine = "ai".
    reason: str | None
    mode: str
    model: str
    prompt_version: str
    latency_ms: int
    calls: int
    ranked: list[AIScoredDisease]
    scores: dict[str, float] = Field(
        description="Every scored disease, 0 if not picked"
    )


@router.post("/score", dependencies=[Depends(get_current_active_superuser)])
def ai_score(body: AIScoreRequest) -> AIScoreResponse:
    """Score answers with the language model. Superusers only: each call spends the
    shared model quota (the app itself uses /triage/flows/{flow_id}/score). Falls back
    to rules, never errors on model trouble. Nothing is saved."""
    try:
        content = get_content_repository().get(body.flow_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Flow not found")
    b = get_ai_engine().score(body.answers.to_domain(), content)
    meta = b.meta
    assert meta is not None
    return AIScoreResponse(
        request_id=meta.request_id,
        engine=meta.engine,
        fallback=meta.fallback,
        reason=meta.reason,
        mode=meta.mode,
        model=meta.model,
        prompt_version=meta.prompt_version,
        latency_ms=meta.latency_ms,
        calls=meta.calls,
        ranked=[
            AIScoredDisease(
                id=r.id,
                score=r.score,
                share=r.share,
                reasons=b.reasons.get(r.id, []),
                sources=meta.sources.get(r.id, []),
            )
            for r in b.ranked
        ],
        scores=b.scores,
    )


class AIDrugsRequest(BaseModel):
    flow_id: Literal["infection", "chronic"] = "infection"
    text: str = Field(max_length=500, description="The patient's free-text drug answer")


class AIDrug(BaseModel):
    mention: str
    generic: str
    # nsaid, antimotilitas, ccb_dhp, acei, statin, diuretik, antikoagulan, lain,
    # tidak_dikenal
    drug_class: str


class AIDrugsResponse(BaseModel):
    request_id: str
    # Classes that can fire a rule in advice.json.
    classes: list[str]
    drugs: list[AIDrug]
    # "ai", "keywords" (every item is a known drug: no model call), "none" (empty
    # text), "fallback" (model not used; the keyword rules still apply).
    engine: str
    fallback: bool
    reason: str | None
    model: str
    latency_ms: int


@router.post("/drugs", dependencies=[Depends(get_current_active_superuser)])
def ai_drugs(body: AIDrugsRequest) -> AIDrugsResponse:
    """Recognize drug classes in free text. Superusers only (spends model quota).
    Never errors on model trouble."""
    recognizer = get_drug_recognizer()
    if recognizer is None:
        r = DrugResult(
            request_id="-",
            classes=[],
            engine="fallback",
            fallback=True,
            reason="model_off",
        )
    else:
        r = recognizer.recognize(body.text, body.flow_id)
    return AIDrugsResponse(
        request_id=r.request_id,
        classes=r.classes,
        drugs=[
            AIDrug(mention=d["mention"], generic=d["generic"], drug_class=d["class"])
            for d in r.drugs
        ],
        engine=r.engine,
        fallback=r.fallback,
        reason=r.reason,
        model=r.model,
        latency_ms=r.latency_ms,
    )


@router.get("/status", dependencies=[Depends(get_current_active_superuser)])
def ai_status() -> dict[str, Any]:
    """Model, mode, and local quota use. Superusers only. No secrets."""
    return get_ai_engine().status()
