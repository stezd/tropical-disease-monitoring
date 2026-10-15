"""Composition root for the triage feature.

The single place where ports, adapters, engines, and use cases are wired together.
Config decisions (which engine, which analyzer) live here instead of leaking into
domain modules.
"""

from app.adapters.outbound.json_files.content_repository import (
    JsonFilesContentRepository,
)
from app.application.ports.outbound.content_repository import ContentRepository
from app.application.use_cases.score_flow import ScoreFlowUseCase
from app.core.config import settings
from app.triage.ai import get_ai_engine
from app.triage.scoring import ModelEngine, RuleEngine, ScoringEngine
from app.triage.vision import PhotoAnalyzer, UnavailableAnalyzer


def get_content_repository() -> ContentRepository:
    """The default content repository (JSON files on disk)."""
    return JsonFilesContentRepository()


def get_scoring_engine() -> ScoringEngine:
    """The configured scoring engine."""
    if settings.TRIAGE_SCORING_ENGINE == "model":
        return ModelEngine(settings.TRIAGE_MODEL_PATH)
    if settings.TRIAGE_SCORING_ENGINE == "ai":
        # Cached: one quota guard per process.
        return get_ai_engine()
    return RuleEngine()


def get_photo_analyzer() -> PhotoAnalyzer:
    """The configured photo analyzer."""
    match settings.TRIAGE_PHOTO_ANALYZER:
        case "none":
            return UnavailableAnalyzer()
        case _:
            return UnavailableAnalyzer()


def get_score_use_case(
    content: ContentRepository | None = None,
    engine: ScoringEngine | None = None,
) -> ScoreFlowUseCase:
    """Construct the score use case with default or injected dependencies."""
    return ScoreFlowUseCase(
        content or get_content_repository(),
        engine or get_scoring_engine(),
    )
