"""Score flow application use case.

Coordinates content loading, engine execution, drug recognition, and patient advice
generation. Decoupled from FastAPI, HTTP status codes, and request parsing.

`preview=True` is for intermediate calls during the quiz (the drug step asks the server
for drug pop-ups before all answers are in). It always scores with the preview engine
(rules), so a language-model engine is only used for the final result.

The drug recognizer, when configured, runs in parallel with scoring and only when a
drug rule could still fire for these answers.
"""

from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass

from app.application.ports.outbound.content_repository import ContentRepository
from app.application.ports.outbound.drug_recognizer import DrugRecognizer
from app.domain.answers import Answers
from app.domain.warnings import drug_classes_wanted
from app.triage.advice import build_result
from app.triage.schemas import ScoreResult
from app.triage.scoring import RuleEngine, ScoringEngine

# Drug recognition never holds the result back longer than this (seconds).
DRUG_WAIT_S = 15.0
_pool = ThreadPoolExecutor(max_workers=8, thread_name_prefix="drugs")


class UnknownFlowError(Exception):
    """The requested flow does not exist."""


class EngineUnavailableError(Exception):
    """The configured scoring engine is not implemented yet."""


@dataclass
class Scored:
    result: ScoreResult
    # What produced the scores: "rules", "model", "ai", or "ai-fb:<reason>".
    engine: str
    drug_classes: frozenset[str]


class ScoreFlowUseCase:
    """The application use case behind the POST /triage/flows/{flow_id}/score endpoint."""

    def __init__(
        self,
        content: ContentRepository,
        engine: ScoringEngine,
        preview_engine: ScoringEngine | None = None,
        drugs: DrugRecognizer | None = None,
    ) -> None:
        self._content = content
        self._engine = engine
        self._preview_engine = preview_engine or RuleEngine()
        self._drugs = drugs

    def execute(
        self, flow_id: str, answers: Answers, preview: bool = False
    ) -> ScoreResult:
        return self.execute_detailed(flow_id, answers, preview).result

    def execute_detailed(
        self, flow_id: str, answers: Answers, preview: bool = False
    ) -> Scored:
        try:
            content = self._content.get(flow_id)
        except KeyError as e:
            raise UnknownFlowError(flow_id) from e

        pending: Future[frozenset[str]] | None = None
        if self._drugs is not None and drug_classes_wanted(answers, content):
            pending = _pool.submit(self._drugs.classes, answers.drugs, flow_id)

        engine = self._preview_engine if preview else self._engine
        try:
            breakdown = engine.score(answers, content)
        except NotImplementedError as e:
            raise EngineUnavailableError(str(e)) from e

        classes: frozenset[str] = frozenset()
        if pending is not None:
            try:
                classes = pending.result(timeout=DRUG_WAIT_S)
            except Exception:  # noqa: BLE001 - timeout or bug: keywords still apply
                classes = frozenset()
        result = build_result(flow_id, answers, content, breakdown, classes)
        return Scored(result, breakdown.engine, classes)
