from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query

from app.adapters.outbound.sqlmodel.screening_repository import (
    SqlModelScreeningRepository,
)
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.application.ports.outbound.screening_repository import ScreeningRepository
from app.application.use_cases.score_flow import (
    EngineUnavailableError,
    Scored,
    UnknownFlowError,
)
from app.composition.triage_container import (
    get_content_repository,
    get_score_use_case,
)
from app.domain.answers import Answers as DomainAnswers
from app.models import Screening, ScreeningPublic, ScreeningsPublic
from app.triage.content import FlowContent
from app.triage.schemas import (
    Answers,
    FlowPublic,
    ScoreResult,
    ScreeningCreate,
    flow_public,
)

router = APIRouter(prefix="/triage", tags=["triage"])


def _content(flow_id: str) -> FlowContent:
    try:
        return get_content_repository().get(flow_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Flow not found")


def score_answers(
    flow_id: str, answers: DomainAnswers, preview: bool = False
) -> ScoreResult:
    """Score answers via the use case. Kept for backwards compatibility."""
    return score_detailed(flow_id, answers, preview).result


def score_detailed(
    flow_id: str, answers: DomainAnswers, preview: bool = False
) -> Scored:
    try:
        return get_score_use_case().execute_detailed(flow_id, answers, preview)
    except UnknownFlowError:
        raise HTTPException(status_code=404, detail="Flow not found")
    except EngineUnavailableError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/flows/{flow_id}")
def read_flow(flow_id: str) -> FlowPublic:
    """Questions and options for a flow. Weights are not included."""
    return flow_public(_content(flow_id))


@router.post("/flows/{flow_id}/score")
def score_flow(
    flow_id: str,
    answers: Answers,
    preview: Annotated[
        bool,
        Query(
            description="True for calls during the quiz (e.g. drug pop-ups at the drug "
            "step): scores with the rules, never with the language model."
        ),
    ] = False,
) -> ScoreResult:
    """Score answers. Stateless: nothing is saved."""
    return score_answers(flow_id, answers.to_domain(), preview)


@router.post("/screenings")
def create_screening(
    session: SessionDep, current_user: CurrentUser, body: ScreeningCreate
) -> ScoreResult:
    """Save a screening for a logged-in user. Only when they agreed (`consent=true`).

    The score is recomputed here with the configured engine, not copied from the
    result the patient saw. With the AI engine the model response is cached by
    the same key as /score (flow + answers), so a save with the same answers is a
    cache hit: same result, no second Gemini call. If the cache entry has expired
    or the engine fell back in between, the saved result can differ from the
    one shown.
    """
    if not body.consent:
        raise HTTPException(status_code=400, detail="Consent is required to save")
    scored = score_detailed(body.flow_id, body.answers.to_domain())
    result = scored.result
    screening = Screening(
        user_id=current_user.id,
        flow_id=body.flow_id,
        answers=body.answers.model_dump(mode="json", exclude_defaults=True),
        route=result.route,
        unknown=result.unknown,
        top_disease=result.top.id if result.top else None,
        top_score=result.top.score if result.top else None,
        # What actually produced the scores ("ai", "rules", "ai-fb:timeout", ...).
        engine=scored.engine[:20],
    )
    repository: ScreeningRepository = SqlModelScreeningRepository(session)
    repository.save(screening)
    return result


@router.get(
    "/screenings",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ScreeningsPublic,
)
def read_screenings(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Saved screenings for ST's analysis. Superusers only."""
    repository: ScreeningRepository = SqlModelScreeningRepository(session)
    rows, count = repository.list(skip, limit)
    return ScreeningsPublic(
        data=[ScreeningPublic.model_validate(r) for r in rows], count=count
    )
