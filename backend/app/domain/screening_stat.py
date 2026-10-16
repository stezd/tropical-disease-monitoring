"""One finished screening as a row of statistics without direct identity.

Pure domain code. The point of this module is the WHITELIST: `StatRecord` lists, field
by field, everything that may be stored for statistics. A new field on `Answers` is NOT
stored until someone adds it here on purpose (a test freezes the field list, so adding
one forces a review).

Never stored: user id, email, name, IP address, creation time, clock time, exact age,
raw vitals (temperature, blood pressure, glucose, height, weight, waist, uric acid,
cholesterol), drug free text, coordinates. Only the date (server calendar day, WIB) is
kept. Combinations of age band, sex, province, and symptoms could in theory still point
to a person, so this is data "tanpa identitas langsung", not anonymous data, and it
stays personal data under UU PDP.

Perlu OK DR: the category cut-offs below (labels only, no effect on score or route).
"""

import re
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from app.domain.answers import Answers
from app.domain.vitals import bp_category, glucose_high
from app.triage.schemas import ScoreResult
from app.triage.scoring import bmi

# Groups smaller than this are hidden when aggregates leave the building.
SMALL_CELL_K = 10

AGE_BANDS = ("0-4", "5-14", "15-24", "25-44", "45-59", "60+")

# Option ids are short ascii tokens. Anything else (e.g. free text pushed into an id
# field) is dropped instead of stored.
_ID = re.compile(r"^[A-Za-z0-9_\-]{1,30}$")
# The 38 provinces, same names as frontend/src/features/triage/location.ts. Anything
# else in the province field is dropped, so free text can never be stored there.
PROVINCES = frozenset(
    {
        "Aceh",
        "Bali",
        "Banten",
        "Bengkulu",
        "DKI Jakarta",
        "Daerah Istimewa Yogyakarta",
        "Gorontalo",
        "Jambi",
        "Jawa Barat",
        "Jawa Tengah",
        "Jawa Timur",
        "Kalimantan Barat",
        "Kalimantan Selatan",
        "Kalimantan Tengah",
        "Kalimantan Timur",
        "Kalimantan Utara",
        "Kepulauan Bangka Belitung",
        "Kepulauan Riau",
        "Lampung",
        "Maluku",
        "Maluku Utara",
        "Nusa Tenggara Barat",
        "Nusa Tenggara Timur",
        "Papua",
        "Papua Barat",
        "Papua Barat Daya",
        "Papua Pegunungan",
        "Papua Selatan",
        "Papua Tengah",
        "Riau",
        "Sulawesi Barat",
        "Sulawesi Selatan",
        "Sulawesi Tengah",
        "Sulawesi Tenggara",
        "Sulawesi Utara",
        "Sumatera Barat",
        "Sumatera Selatan",
        "Sumatera Utara",
    }
)
_MAX_IDS = 30


def age_band(age: int | None) -> str | None:
    if age is None:
        return None
    if age <= 4:
        return "0-4"
    if age <= 14:
        return "5-14"
    if age <= 24:
        return "15-24"
    if age <= 44:
        return "25-44"
    if age <= 59:
        return "45-59"
    return "60+"


def temp_category(temp: float | None) -> str | None:
    """normal < 37.5 · demam 37.5 to < 39.5 · demam tinggi >= 39.5 (the route rule)."""
    if temp is None:
        return None
    if temp >= 39.5:
        return "demam tinggi"
    if temp >= 37.5:
        return "demam"
    return "normal"


def bmi_category(answers: Answers) -> str | None:
    """kurus < 18.5 · normal < 25 · gemuk < 30 · obes >= 30. None without usable data."""
    b = bmi(answers)
    if b is None:
        return None
    if b < 18.5:
        return "kurus"
    if b < 25:
        return "normal"
    if b < 30:
        return "gemuk"
    return "obes"


@dataclass(frozen=True)
class StatRecord:
    """The whitelist. Add a field here only after DR/privacy review."""

    event_id: UUID
    day: date
    flow_id: str
    route: str
    unknown: bool
    top_disease: str | None
    top_score: float | None
    others: list[str]
    engine: str
    who: str | None
    sex: str | None
    age_band: str | None
    pregnant: bool | None
    province: str | None
    complaint: str | None
    pattern: str | None
    red_flags: list[str] = field(default_factory=list)
    companion: list[str] = field(default_factory=list)
    eco: list[str] = field(default_factory=list)
    body: list[str] = field(default_factory=list)
    vital_proxy: list[str] = field(default_factory=list)
    nutrition_proxy: str | None = None
    pain: int | None = None
    temp_cat: str | None = None
    bp_cat: str | None = None
    glucose_high: bool = False
    bmi_cat: str | None = None
    no_thermo: bool = False
    no_bp: bool = False
    # Whether any drug was typed. The text itself is never kept.
    drugs_given: bool = False


def _id(value: str | None) -> str | None:
    return value if value is not None and _ID.match(value) else None


def _ids(values: list[str]) -> list[str]:
    return [v for v in values[:_MAX_IDS] if _ID.match(v)]


def to_stat(
    answers: Answers,
    result: ScoreResult,
    engine: str,
    day: date,
    event_id: UUID,
) -> StatRecord:
    """Build the stored record from answers and result. Whitelist, field by field."""
    province = answers.province.strip() if answers.province else None
    bp = (
        bp_category(answers.bp_sys, answers.bp_dia)
        if answers.bp_sys is not None and answers.bp_dia is not None
        else None
    )
    return StatRecord(
        event_id=event_id,
        day=day,
        flow_id=result.flow_id,
        route=result.route,
        unknown=result.unknown,
        top_disease=result.top.id if result.top else None,
        top_score=round(result.top.score, 1) if result.top else None,
        others=[o.id for o in result.others[:3]],
        engine=engine[:20],
        who=_id(answers.who),
        sex=answers.sex,
        age_band=age_band(answers.age),
        pregnant=answers.pregnant,
        province=province if province in PROVINCES else None,
        complaint=_id(answers.complaint),
        pattern=_id(answers.pattern),
        red_flags=_ids(answers.red_flags),
        companion=_ids(answers.companion),
        eco=_ids(answers.eco),
        body=_ids(answers.body),
        vital_proxy=_ids(answers.vital_proxy),
        nutrition_proxy=answers.nutrition_proxy,
        pain=answers.pain,
        temp_cat=temp_category(answers.temp),
        bp_cat=bp,
        glucose_high=glucose_high(answers.glucose),
        bmi_cat=bmi_category(answers),
        no_thermo=answers.no_thermo,
        no_bp=answers.no_bp,
        drugs_given=bool(answers.drugs.strip()),
    )
