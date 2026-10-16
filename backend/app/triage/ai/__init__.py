"""AI scoring service. Owned by the AI engineer; ST wires it in.

A language model (Gemini by default, swappable by config) scores disease candidates
from the patient's facts plus pre-retrieved literature. RuleEngine stays the safety net:
any timeout, quota, or invalid output falls back to it, and the result says so.

Entry points:
- `get_ai_engine()`: a ScoringEngine for TRIAGE_SCORING_ENGINE=ai (same interface as RuleEngine).
- `AIEngine.score(answers, content) -> AIBreakdown`: a ScoreBreakdown plus `meta`
  (engine actually used, fallback flag and reason, model, latency).
- HTTP: POST /api/v1/ai/score (app/api/routes/ai.py).

Settings: env vars with prefix TRIAGE_AI_ (see config.py). Guide: README.md in this folder.
"""

from app.triage.ai.engine import AIBreakdown, AIEngine, AIMeta, get_ai_engine

__all__ = ["AIBreakdown", "AIEngine", "AIMeta", "get_ai_engine"]
