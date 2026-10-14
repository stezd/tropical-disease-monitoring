"""Score flow application use case.

Coordinates content loading, engine execution, and patient advice generation.
Decoupled from FastAPI, HTTP status codes, and request parsing.
"""

from app.application.ports.outbound.content_repository import ContentRepository
from app.domain.answers import Answers
from app.triage.advice import build_result
from app.triage.schemas import ScoreResult
from app.triage.scoring import ScoringEngine


class UnknownFlowError(Exception):
    """The requested flow does not exist."""


class EngineUnavailableError(Exception):
    """The configured scoring engine is not implemented yet."""


class ScoreFlowUseCase:
    """The application use case behind the POST /triage/flows/{flow_id}/score endpoint."""

    def __init__(self, content: ContentRepository, engine: ScoringEngine) -> None:
        self._content = content
        self._engine = engine

    def execute(self, flow_id: str, answers: Answers) -> ScoreResult:
        try:
            content = self._content.get(flow_id)
        except KeyError as e:
            raise UnknownFlowError(flow_id) from e
        try:
            breakdown = self._engine.score(answers, content)
        except NotImplementedError as e:
            raise EngineUnavailableError(str(e)) from e
        return build_result(flow_id, answers, content, breakdown)
