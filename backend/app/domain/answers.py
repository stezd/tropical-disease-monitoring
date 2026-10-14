"""Domain value object for quiz answers.

Everything the patient answered. Never holds a name, NIK, BPJS number, or photo.
Option IDs in `Answers` match the IDs used in content/<flow>/*.json and in the front end.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

IdList = list[str]


class Answers(BaseModel):
    """Everything the patient answered."""

    who: str | None = Field(default=None, max_length=20)
    age: int | None = Field(default=None, ge=0, le=120)
    sex: Literal["L", "P"] | None = None
    # Asked only for women (flow.pregnancy_from_age). Not scored yet.
    pregnant: bool | None = None
    red_flags: IdList = Field(default_factory=list, max_length=20)
    # A cluster ID, or "none" when the flow allows no complaint (chronic risk check).
    complaint: str | None = Field(default=None, max_length=4)
    pattern: str | None = Field(default=None, max_length=20)
    companion: IdList = Field(default_factory=list, max_length=20)
    eco: IdList = Field(default_factory=list, max_length=20)
    drugs: str = Field(default="", max_length=500)
    temp: float | None = Field(default=None, ge=34, le=43)
    no_thermo: bool = False
    bp_sys: int | None = Field(default=None, ge=50, le=300)
    bp_dia: int | None = Field(default=None, ge=30, le=200)
    no_bp: bool = False
    glucose: float | None = Field(default=None, ge=10, le=1000)
    # Stand-in answers when there is no thermometer or blood pressure meter.
    vital_proxy: IdList = Field(default_factory=list, max_length=20)
    height_cm: float | None = Field(default=None, ge=0, le=300)
    weight_kg: float | None = Field(default=None, ge=0, le=500)
    waist_cm: float | None = Field(default=None, ge=0, le=250)
    nutrition_proxy: Literal["longgar", "gemuk", "normal"] | None = None
    body: IdList = Field(default_factory=list, max_length=20)
    pain: int | None = Field(default=None, ge=0, le=10)
    findings: IdList = Field(default_factory=list, max_length=20)
    # Province name only, never coordinates. Pending DR + ST (AGENTS.md, question no. 10).
    province: str | None = Field(default=None, max_length=64)
    # When the patient finished the quiz, with their UTC offset. Used in the summary.
    taken_at: datetime | None = None
