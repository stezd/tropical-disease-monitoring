"""Composition root for the triage feature.

The single place where ports, adapters, engines, and use cases are wired together.
Config decisions (which engine) live here instead of leaking into domain modules.
"""

from typing import Literal

from app.adapters.outbound.json_files.content_repository import (
    JsonFilesContentRepository,
)
from app.application.ports.outbound.content_repository import ContentRepository
from app.application.ports.outbound.drug_recognizer import DrugRecognizer
from app.application.use_cases.score_flow import ScoreFlowUseCase
from app.core.config import settings
from app.triage.ai import get_ai_engine
from app.triage.ai.drugs import get_drug_recognizer
from app.triage.scoring import ModelEngine, RuleEngine, ScoringEngine


def get_content_repository() -> ContentRepository:
    """The default content repository (JSON files on disk)."""
    return JsonFilesContentRepository()


def get_scoring_engine() -> ScoringEngine:
    """The configured scoring engine."""
    if settings.TRIAGE_SCORING_ENGINE == "model":
        return ModelEngine(settings.TRIAGE_MODEL_PATH)
    if settings.TRIAGE_SCORING_ENGINE == "ai":
        # Cached: one quota guard and one result cache per process.
        return get_ai_engine()
    return RuleEngine()


def get_drug_recognizer_port() -> DrugRecognizer | None:
    """Drug recognition for the drug pop-ups, or None (keywords only).

    Independent of the scoring engine: on whenever TRIAGE_AI_DRUGS_ENABLED and a model
    key are set, also with TRIAGE_SCORING_ENGINE=rules. Cached: shares the quota guard.
    """
    return get_drug_recognizer()


def get_score_use_case(
    content: ContentRepository | None = None,
    engine: ScoringEngine | None = None,
    drugs: DrugRecognizer | None | Literal["default"] = "default",
) -> ScoreFlowUseCase:
    """Construct the score use case with default or injected dependencies.

    Preview calls (during the quiz) always score with RuleEngine.
    """
    return ScoreFlowUseCase(
        content or get_content_repository(),
        engine or get_scoring_engine(),
        preview_engine=RuleEngine(),
        drugs=get_drug_recognizer_port() if drugs == "default" else drugs,
    )
