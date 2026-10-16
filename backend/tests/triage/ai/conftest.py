"""Keep the AI tests hermetic.

AISettings points at ../.env, so a developer who configures AI locally (as the
README tells them to) would silently change what these tests assert: with a real
TRIAGE_AI_PROVIDER in .env, `AISettings(API_KEY="")` builds a client instead of
returning None. Tests construct their settings explicitly, so the file must not
take part. (`_env_file=None` per call would do the same; this covers them all.)
"""

import pytest

from app.triage.ai.config import AISettings


@pytest.fixture(autouse=True)
def _ignore_dotenv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(AISettings.model_config, "env_file", None)
