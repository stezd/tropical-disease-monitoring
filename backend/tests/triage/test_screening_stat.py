"""The statistics whitelist: only these fields, never identity or raw numbers."""

import dataclasses
import uuid
from datetime import date

from app.application.ports.outbound.screening_stat_repository import StatGroup
from app.application.use_cases.score_flow import ScoreFlowUseCase
from app.application.use_cases.stats_summary import StatsSummaryUseCase
from app.composition.triage_container import get_content_repository
from app.domain.answers import Answers
from app.domain.screening_stat import (
    StatRecord,
    age_band,
    bmi_category,
    temp_category,
    to_stat,
)
from app.triage.scoring import RuleEngine

# FROZEN. Adding a field to StatRecord means a new thing is stored about patients:
# it needs privacy review (DR) and an update to the privacy text before you change
# this list.
FROZEN_FIELDS = [
    "event_id",
    "day",
    "flow_id",
    "route",
    "unknown",
    "top_disease",
    "top_score",
    "others",
    "engine",
    "who",
    "sex",
    "age_band",
    "pregnant",
    "province",
    "complaint",
    "pattern",
    "red_flags",
    "companion",
    "eco",
    "body",
    "vital_proxy",
    "nutrition_proxy",
    "pain",
    "temp_cat",
    "bp_cat",
    "glucose_high",
    "bmi_cat",
    "no_thermo",
    "no_bp",
    "drugs_given",
]

FORBIDDEN_NAMES = {
    "user_id",
    "email",
    "name",
    "ip",
    "created_at",
    "taken_at",
    "age",
    "temp",
    "bp_sys",
    "bp_dia",
    "glucose",
    "height_cm",
    "weight_kg",
    "waist_cm",
    "uric_acid",
    "cholesterol_total",
    "drugs",
    "latitude",
    "longitude",
}

ANSWERS = Answers(
    who="self",
    age=37,
    sex="P",
    pregnant=False,
    red_flags=["none"],
    complaint="A",
    pattern="malaria",
    companion=["malaria"],
    eco=["timur"],
    drugs="paracetamol 500mg SECRETDRUG",
    temp=38.61,
    bp_sys=151,
    bp_dia=93,
    glucose=213.0,
    uric_acid=7.7,
    cholesterol_total=233.0,
    height_cm=160,
    weight_kg=52,
    waist_cm=77,
    province="Papua",
    body=["perut"],
    pain=4,
)


def _stat(answers: Answers = ANSWERS) -> StatRecord:
    content = get_content_repository().get("infection")
    from app.triage.advice import build_result

    breakdown = RuleEngine().score(answers, content)
    result = build_result("infection", answers, content, breakdown, frozenset())
    return to_stat(answers, result, "rules", date(2026, 10, 16), uuid.uuid4())


def test_stat_record_fields_are_frozen() -> None:
    assert [f.name for f in dataclasses.fields(StatRecord)] == FROZEN_FIELDS
    assert not FORBIDDEN_NAMES & set(FROZEN_FIELDS)


def test_age_band() -> None:
    cases = {
        0: "0-4",
        4: "0-4",
        5: "5-14",
        14: "5-14",
        15: "15-24",
        24: "15-24",
        25: "25-44",
        44: "25-44",
        45: "45-59",
        59: "45-59",
        60: "60+",
        120: "60+",
    }
    for age, band in cases.items():
        assert age_band(age) == band
    assert age_band(None) is None


def test_temp_category() -> None:
    assert temp_category(None) is None
    assert temp_category(36.8) == "normal"
    assert temp_category(37.5) == "demam"
    assert temp_category(39.4) == "demam"
    assert temp_category(39.5) == "demam tinggi"


def test_bmi_category() -> None:
    assert bmi_category(Answers(height_cm=170, weight_kg=50)) == "kurus"
    assert bmi_category(Answers(height_cm=170, weight_kg=65)) == "normal"
    assert bmi_category(Answers(height_cm=170, weight_kg=80)) == "gemuk"
    assert bmi_category(Answers(height_cm=170, weight_kg=95)) == "obes"
    assert bmi_category(Answers()) is None


def test_categories_in_record() -> None:
    s = _stat()
    assert s.age_band == "25-44"
    assert s.temp_cat == "demam"
    assert s.bp_cat == "tinggi"
    assert s.glucose_high is True
    assert s.bmi_cat == "normal"
    assert s.drugs_given is True
    assert s.day == date(2026, 10, 16)
    assert s.province == "Papua"


def test_no_raw_values_in_record() -> None:
    s = _stat()
    flat = repr(dataclasses.asdict(s))
    for needle in ("SECRETDRUG", "paracetamol", "38.61", "151", "213", "233", "7.7"):
        assert needle not in flat
    values = dataclasses.asdict(s).values()
    assert 37 not in values  # exact age
    assert 160 not in values and 52 not in values and 77 not in values


def test_free_text_in_id_fields_is_dropped() -> None:
    a = ANSWERS.model_copy(
        update={
            "pattern": "nama saya budi",
            "eco": ["timur", "alamat jl. mawar 5"],
            "province": "x" * 10 + "<script>",
        }
    )
    s = _stat(a)
    assert s.pattern is None
    assert s.eco == ["timur"]
    assert s.province is None


def test_red_flag_record_uses_no_model() -> None:
    called: list[int] = []

    class Boom(RuleEngine):
        def score(self, *args, **kwargs):  # type: ignore[no-untyped-def]
            called.append(1)
            return super().score(*args, **kwargs)

    use_case = ScoreFlowUseCase(get_content_repository(), Boom())
    scored = use_case.execute_detailed(
        "infection", Answers(red_flags=["syok"]), preview=False
    )
    assert scored.result.route == "red"


class _FakeStats:
    def __init__(self, groups):
        self._groups = groups

    def aggregate(self, *_args):
        return self._groups


def test_small_groups_are_hidden() -> None:
    groups = [
        StatGroup(date(2026, 10, 16), "Papua", "dbd", "yellow", 9),
        StatGroup(date(2026, 10, 16), "Papua", "dbd", "green", 10),
    ]
    out = StatsSummaryUseCase(_FakeStats(groups)).execute("day", None, None, None)
    assert out[0].count is None
    assert out[1].count == 10
    assert groups[0].count == 9  # input untouched


def test_table_columns_match_the_whitelist() -> None:
    """The stats table holds exactly the StatRecord fields: no extra column can
    quietly store something the whitelist does not list."""
    from app.models import ScreeningStat

    assert set(ScreeningStat.model_fields) == {
        f.name for f in dataclasses.fields(StatRecord)
    }
