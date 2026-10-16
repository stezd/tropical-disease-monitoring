"""Request and response models for the triage API.

Option IDs in `Answers` are the same IDs used in content/*.json and in the front end.
"""

from pydantic import BaseModel, Field

from app.domain.answers import Answers as DomainAnswers
from app.domain.answers import IdList as IdList
from app.triage.content import Flow, FlowContent, RouteId, WarningLevel
from app.triage.scoring import EngineId


# ponytail: the inbound DTO keeps the public name `Answers` (frozen OpenAPI contract) and
# subclasses the domain VO, so `to_domain()` is a real mapping while callers stay source
# compatible. Give it its own copy of the fields if the API and domain shapes diverge (D1c).
class Answers(DomainAnswers):
    """Everything the patient answered. Never holds a name, NIK, BPJS number, or
    coordinates."""

    def to_domain(self) -> DomainAnswers:
        return DomainAnswers.model_validate(self.model_dump())


class DiseasePublic(BaseModel):
    name: str
    emoji: str
    route: RouteId


class FlowPublic(Flow):
    diseases: dict[str, DiseasePublic]


class RankedDisease(BaseModel):
    id: str
    name: str
    emoji: str
    score: float
    pct: int


class Warning(BaseModel):
    level: WarningLevel
    icon: str
    text: str


class SummaryRow(BaseModel):
    # Stable id for the front end (e.g. "lab", "red_flags"); label and value are shown.
    key: str
    label: str
    value: str


class ScoreResult(BaseModel):
    flow_id: str
    route: RouteId
    # True when the top score is below the threshold: "belum dapat ditentukan", route SEDANG.
    unknown: bool
    top: RankedDisease | None
    others: list[RankedDisease]
    # Mascot meter during the quiz.
    meter_candidates: int
    meter_pct: int
    reasons: list[str]
    cross_checks: list[str]
    warnings: list[Warning]
    # Shown as a pop-up right after the drug step.
    drug_popups: list[Warning]
    todo: list[str]
    place: str
    maps_query: str
    nav_label: str
    analysis_steps: list[str]
    # Plain text for copying, and the same content as rows for the QR page.
    summary: str
    summary_rows: list[SummaryRow]
    # The engine that produced the scores: "ai" (language model), "rules" (RuleEngine),
    # or "model" (ST's trained model). `fallback` = the configured engine failed and
    # RuleEngine answered instead. Not shown to the patient.
    engine: EngineId
    fallback: bool


class ScreeningCreate(BaseModel):
    flow_id: str = Field(max_length=20)
    answers: Answers
    consent: bool = Field(description="Must be true. The patient agreed to save.")


def flow_public(content: FlowContent) -> FlowPublic:
    """What the front end gets: questions and public disease info. No weights or lab."""
    return FlowPublic(
        **content.flow.model_dump(),
        diseases={
            k: DiseasePublic(name=d.name, emoji=d.emoji, route=d.route)
            for k, d in content.diseases.items()
        },
    )
