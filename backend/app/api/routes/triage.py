from typing import Annotated, Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import col, func, select

from app.api.deps import SessionDep, get_current_active_superuser
from app.core.config import settings
from app.models import Screening, ScreeningPublic, ScreeningsPublic
from app.triage.advice import build_result
from app.triage.content import FlowContent, get_content
from app.triage.schemas import (
    Answers,
    FlowPublic,
    PhotoAnalysis,
    ScoreResult,
    ScreeningCreate,
    flow_public,
)
from app.triage.scoring import get_engine
from app.triage.vision import ALLOWED_TYPES, MAX_PHOTO_BYTES, get_analyzer

router = APIRouter(prefix="/triage", tags=["triage"])


def _content(flow_id: str) -> FlowContent:
    try:
        return get_content(flow_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Flow not found")


def score_answers(flow_id: str, answers: Answers) -> ScoreResult:
    content = _content(flow_id)
    try:
        breakdown = get_engine().score(answers, content)
    except NotImplementedError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return build_result(flow_id, answers, content, breakdown)


@router.get("/flows/{flow_id}")
def read_flow(flow_id: str) -> FlowPublic:
    """Questions and options for a flow. Weights are not included."""
    return flow_public(_content(flow_id))


@router.post("/flows/{flow_id}/score")
def score_flow(flow_id: str, answers: Answers) -> ScoreResult:
    """Score answers. Stateless: nothing is saved."""
    return score_answers(flow_id, answers)


@router.post("/screenings")
def create_screening(session: SessionDep, body: ScreeningCreate) -> ScoreResult:
    """Save an anonymous screening. Only when the patient agreed (`consent=true`)."""
    if not body.consent:
        raise HTTPException(status_code=400, detail="Consent is required to save")
    result = score_answers(body.flow_id, body.answers)
    screening = Screening(
        flow_id=body.flow_id,
        answers=body.answers.model_dump(mode="json", exclude_defaults=True),
        route=result.route,
        unknown=result.unknown,
        top_disease=result.top.id if result.top else None,
        top_score=result.top.score if result.top else None,
        engine=settings.TRIAGE_SCORING_ENGINE,
    )
    session.add(screening)
    session.commit()
    return result


@router.get(
    "/screenings",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=ScreeningsPublic,
)
def read_screenings(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """Saved screenings for ST's analysis. Superusers only."""
    count = session.exec(select(func.count()).select_from(Screening)).one()
    rows = session.exec(
        select(Screening)
        .order_by(col(Screening.created_at).desc())
        .offset(skip)
        .limit(limit)
    ).all()
    return ScreeningsPublic(
        data=[ScreeningPublic.model_validate(r) for r in rows], count=count
    )


@router.post("/photo/analyze")
def analyze_photo(
    photo: Annotated[UploadFile, File(description="Rash, wound, tongue, or eye")],
) -> PhotoAnalysis:
    """Find visible signs in a photo. The photo is never stored.

    Skeleton: returns `available=false` until ST plugs in a model (app/triage/vision.py).
    """
    analyzer = get_analyzer()
    if not analyzer.available:
        return PhotoAnalysis(
            available=False, findings=[], message="Analisis foto belum tersedia."
        )
    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported image type")
    data = photo.file.read(MAX_PHOTO_BYTES + 1)
    if len(data) > MAX_PHOTO_BYTES:
        raise HTTPException(status_code=413, detail="Photo too large")
    findings = analyzer.analyze(data, photo.content_type)
    return PhotoAnalysis(available=True, findings=findings, message="")
