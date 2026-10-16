"""Low confidence: top guess below `refer_below_pct` raises GREEN to YELLOW + a note."""

import pytest

from app.domain.route_policy import decide_route
from app.triage.content import FlowContent, get_content
from app.triage.schemas import Answers
from app.triage.scoring import ScoreBreakdown, rank

GREEN = "scabies"
SPECIAL = "campak"


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


def breakdown(content: FlowContent, scores: dict[str, float]) -> ScoreBreakdown:
    ranked = rank(scores, content.weights.softmax_temperature)
    return ScoreBreakdown(scores=scores, reasons={}, ranked=ranked)


def with_pct(content: FlowContent, top_id: str, pct: int) -> ScoreBreakdown:
    """A breakdown whose top guess shows exactly `pct` percent."""
    b = breakdown(content, {top_id: 80.0, "dbd": 40.0})
    b.ranked[0].share = pct / 100
    return b


def answers() -> Answers:
    return Answers.model_validate(
        {"red_flags": ["none"], "age": 30, "no_thermo": True, "no_bp": True}
    )


def decide(
    content: FlowContent, b: ScoreBreakdown, flags: list[str] | None = None
) -> tuple[str, bool, list[str]]:
    return decide_route(answers(), content, b, flags or [])


def test_content_has_threshold_and_text(content: FlowContent) -> None:
    assert content.weights.refer_below_pct == 80
    assert content.advice.warnings.low_confidence
    assert get_content("chronic").weights.refer_below_pct == 80
    assert get_content("chronic").advice.warnings.low_confidence


def test_green_below_threshold_goes_yellow_with_note(content: FlowContent) -> None:
    route, unknown, notes = decide(content, with_pct(content, GREEN, 79))
    assert (route, unknown) == ("yellow", False)
    assert len(notes) == 1 and "79%" in notes[0]


def test_at_threshold_no_change(content: FlowContent) -> None:
    route, unknown, notes = decide(content, with_pct(content, GREEN, 80))
    assert (route, unknown, notes) == ("green", False, [])


def test_special_route_unchanged_but_noted(content: FlowContent) -> None:
    route, _, notes = decide(content, with_pct(content, SPECIAL, 60))
    assert route == "special"
    assert len(notes) == 1


def test_red_flag_unchanged_without_note(content: FlowContent) -> None:
    route, unknown, notes = decide(content, with_pct(content, GREEN, 40), ["napas"])
    assert (route, unknown, notes) == ("red", False, [])


def test_unknown_stays_yellow_without_note(content: FlowContent) -> None:
    b = breakdown(content, {GREEN: content.weights.low_score_threshold - 1})
    route, unknown, notes = decide(content, b)
    assert (route, unknown, notes) == ("yellow", True, [])


def test_feature_off_keeps_old_behaviour(content: FlowContent) -> None:
    off = content.model_copy(
        update={"weights": content.weights.model_copy(update={"refer_below_pct": None})}
    )
    route, _, notes = decide(off, with_pct(off, GREEN, 10))
    assert (route, notes) == ("green", [])


def test_missing_text_still_raises_route(content: FlowContent) -> None:
    wn = content.advice.warnings.model_copy(update={"low_confidence": None})
    advice = content.advice.model_copy(update={"warnings": wn})
    no_text = content.model_copy(update={"advice": advice})
    route, _, notes = decide(no_text, with_pct(no_text, GREEN, 50))
    assert (route, notes) == ("yellow", [])


def test_ai_style_scores_clear_top_no_upgrade(content: FlowContent) -> None:
    # LLM scores 70 / 30 (about 88% after softmax).
    b = breakdown(content, {GREEN: 70.0, "dbd": 30.0})
    assert round(b.ranked[0].share * 100) >= 80
    route, _, notes = decide(content, b)
    assert (route, notes) == ("green", [])


def test_ai_style_scores_close_race_upgrade(content: FlowContent) -> None:
    # LLM scores 50 / 45 (about 56%).
    b = breakdown(content, {GREEN: 50.0, "dbd": 45.0})
    assert round(b.ranked[0].share * 100) < 80
    route, _, notes = decide(content, b)
    assert route == "yellow"
    assert len(notes) == 1
