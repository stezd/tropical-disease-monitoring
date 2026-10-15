"""Unit tests for the application use case and composition root.

Proves ScoreFlowUseCase is genuinely decoupled from disk and from the concrete
engine via the outbound ports (closes finding H8).
"""

import pytest

from app.application.use_cases.score_flow import (
    EngineUnavailableError,
    ScoreFlowUseCase,
    UnknownFlowError,
)
from app.composition.triage_container import (
    get_content_repository,
    get_preview_use_case,
    get_score_use_case,
    get_scoring_engine,
)
from app.core.config import settings
from app.domain.answers import Answers
from app.domain.triage_content import FlowContent
from app.triage.content import get_content
from app.triage.scoring import RuleEngine, ScoreBreakdown


class FakeContentRepository:
    """In-memory content port. Duck-typed: no disk, no caching."""

    def __init__(self, content: FlowContent | None = None) -> None:
        self._content = content

    def get(self, flow_id: str) -> FlowContent:
        if self._content is None or flow_id != self._content.flow.id:
            raise KeyError(flow_id)
        return self._content


class TrackingEngine:
    """Scoring port that records its call and delegates to the real rules."""

    def __init__(self) -> None:
        self.called_with: tuple[Answers, FlowContent] | None = None
        self._real = RuleEngine()

    def score(self, answers: Answers, content: FlowContent) -> ScoreBreakdown:
        self.called_with = (answers, content)
        return self._real.score(answers, content)


class UnimplementedEngine:
    def score(self, answers: Answers, content: FlowContent) -> ScoreBreakdown:
        raise NotImplementedError("not configured")


def test_use_case_runs_against_fake_ports() -> None:
    """The use case works with test doubles — no real file adapter, injected engine."""
    content = get_content("infection")
    engine = TrackingEngine()
    use_case = ScoreFlowUseCase(FakeContentRepository(content), engine)

    answers = Answers(complaint="A", pattern="dbd", temp=38.5)
    result = use_case.execute("infection", answers)

    assert result.flow_id == "infection"
    # The injected engine is the one that ran, with the domain VO we passed.
    assert engine.called_with == (answers, content)
    assert result.top is not None


def test_use_case_raises_on_unknown_flow() -> None:
    use_case = ScoreFlowUseCase(FakeContentRepository(), TrackingEngine())
    with pytest.raises(UnknownFlowError):
        use_case.execute("nonexistent", Answers())


def test_use_case_raises_on_unimplemented_engine() -> None:
    use_case = ScoreFlowUseCase(
        FakeContentRepository(get_content("infection")), UnimplementedEngine()
    )
    with pytest.raises(EngineUnavailableError):
        use_case.execute("infection", Answers())


def test_composition_container_resolves_defaults() -> None:
    assert get_content_repository() is not None
    assert get_scoring_engine() is not None
    assert get_score_use_case() is not None


def test_preview_use_case_always_uses_rules(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "TRIAGE_SCORING_ENGINE", "model")
    result = get_preview_use_case().execute(
        "infection", Answers(complaint="A", pattern="dbd", temp=38.5)
    )
    assert (result.engine, result.fallback) == ("rules", False)


def test_default_use_case_scores_a_real_flow() -> None:
    result = get_score_use_case().execute(
        "infection", Answers(complaint="A", pattern="dbd", temp=38.5)
    )
    assert result.flow_id == "infection"
    assert result.top is not None
