"""Request and response models for the triage API.

Option IDs in `Answers` are the same IDs used in content/*.json and in the front end.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.triage.content import Flow, FlowContent, RouteId

IdList = list[str]


class Answers(BaseModel):
    """Everything the patient answered. Never holds a name, NIK, BPJS number, or photo."""

    who: str | None = Field(default=None, max_length=20)
    age: int | None = Field(default=None, ge=0, le=120)
    sex: Literal["L", "P"] | None = None
    red_flags: IdList = Field(default_factory=list, max_length=20)
    complaint: str | None = Field(default=None, max_length=4)
    pattern: str | None = Field(default=None, max_length=20)
    companion: IdList = Field(default_factory=list, max_length=20)
    eco: IdList = Field(default_factory=list, max_length=20)
    drugs: str = Field(default="", max_length=500)
    temp: float | None = Field(default=None, ge=34, le=43)
    no_thermo: bool = False
    height_cm: float | None = Field(default=None, ge=0, le=300)
    weight_kg: float | None = Field(default=None, ge=0, le=500)
    nutrition_proxy: Literal["longgar", "gemuk", "normal"] | None = None
    body: IdList = Field(default_factory=list, max_length=20)
    pain: int | None = Field(default=None, ge=0, le=10)
    findings: IdList = Field(default_factory=list, max_length=20)
    # Province name only, never coordinates. Pending DR + ST (AGENTS.md, question no. 10).
    province: str | None = Field(default=None, max_length=64)
    # When the patient finished the quiz, with their UTC offset. Used in the summary.
    taken_at: datetime | None = None


class DiseasePublic(BaseModel):
    name: str
    emoji: str
    route: RouteId


class FlowPublic(Flow):
    diseases: dict[str, DiseasePublic]
    # False = photo stays on the device and the patient picks findings (simulated step).
    photo_analysis: bool


class RankedDisease(BaseModel):
    id: str
    name: str
    emoji: str
    score: float
    pct: int


class Warning(BaseModel):
    level: Literal["y", "r", "b"]
    icon: str
    text: str


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
    drug_popups: list[str]
    todo: list[str]
    place: str
    maps_query: str
    nav_label: str
    analysis_steps: list[str]
    summary: str


class ScreeningCreate(BaseModel):
    flow_id: str = Field(max_length=20)
    answers: Answers
    consent: bool = Field(description="Must be true. The patient agreed to save.")


class PhotoAnalysis(BaseModel):
    available: bool
    findings: list[str]
    message: str


def flow_public(content: FlowContent, photo_analysis: bool = False) -> FlowPublic:
    """What the front end gets: questions and public disease info. No weights or lab."""
    return FlowPublic(
        **content.flow.model_dump(),
        diseases={
            k: DiseasePublic(name=d.name, emoji=d.emoji, route=d.route)
            for k, d in content.diseases.items()
        },
        photo_analysis=photo_analysis,
    )
