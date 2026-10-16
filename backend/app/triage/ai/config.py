"""Settings for the AI scoring service. Env prefix TRIAGE_AI_ (e.g. TRIAGE_AI_API_KEY).

Kept apart from app.core.config so these modules load and test without database
settings. Changing the model or provider is a config change only: the backend code and
the API stay the same.
"""

from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DATA_DIR = Path(__file__).parent / "data"

Provider = Literal["gemini", "openai_compat", "off"]
Mode = Literal["single", "per_candidate"]


class AISettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TRIAGE_AI_",
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # "gemini" = Google AI Studio API. "openai_compat" = any OpenAI-style server
    # (e.g. vLLM serving Gemma4 on a GPU). "off" = always use RuleEngine.
    PROVIDER: Provider = "gemini"
    # Flash-Lite answered reliably on the free tier (15 Oct 2026); gemini-3.6-flash
    # answered 503 three times in a row. Flash can be the main model with Flash-Lite
    # as FALLBACK_MODEL once it is reachable.
    MODEL: str = "gemini-3.5-flash-lite"
    # Gemini: tried once when MODEL answers 503 or 429. openai_compat: sent as
    # OpenRouter's `models` fallback list (OpenRouter only; vLLM ignores or rejects it).
    # Empty = no second model.
    FALLBACK_MODEL: str = ""
    API_KEY: SecretStr = SecretStr("")
    # Empty = the provider's default. Required for openai_compat (".../v1").
    BASE_URL: str = ""
    # Gateways that police abuse want to know who is calling. OpenCode Go
    # (https://opencode.ai/docs/go/#where-can-i-use-it) requires a stable session
    # id in `x-opencode-session` and a client user agent of its own, not httpx's.
    SESSION_ID: str = ""
    USER_AGENT: str = ""
    # openai_compat only. Also write the output JSON Schema into the system message.
    # Turn on for endpoints that accept `response_format` but do not enforce the schema,
    # e.g. OpenRouter's google/gemma-4-26b-a4b-it:free (no `structured_outputs`).
    SCHEMA_IN_PROMPT: bool = False
    # Gemini 3.x thinking level. "" = model default. Lower = faster, fewer tokens.
    THINKING_LEVEL: Literal["", "minimal", "low", "medium", "high"] = "low"
    # Empty = the model's default. Google strongly recommends the default (1.0) for
    # Gemini 3: lower values can cause looping or degraded reasoning.
    TEMPERATURE: float | None = Field(default=None, ge=0, le=2)

    # "single" = all candidates in one call (1 request per patient).
    # "per_candidate" = one call per shortlisted candidate (about 3 to 6 requests).
    MODE: Mode = "single"
    # Per-candidate shortlist: members of the chosen cluster + this many RuleEngine top scores.
    SHORTLIST_RULE_TOP: int = Field(default=2, ge=0, le=10)
    # Literature excerpts per candidate. Single mode sends one set for every candidate.
    SOURCES_PER_CANDIDATE: int = Field(default=3, ge=0, le=8)
    SOURCES_PER_CANDIDATE_SINGLE: int = Field(default=1, ge=0, le=4)

    # Seconds. One model call, and the whole scoring including retries.
    CALL_TIMEOUT_S: float = Field(default=15.0, gt=0)
    DEADLINE_S: float = Field(default=20.0, gt=0)
    # Retries after a network error or 5xx. Never after 429 or a timeout.
    RETRIES: int = Field(default=1, ge=0, le=3)
    MAX_PARALLEL: int = Field(default=6, ge=1, le=20)

    # Local quota guard, per server process. Set from the limits AI Studio shows for
    # your project (Google no longer publishes free-tier numbers). 0 = no guard.
    RPM_LIMIT: int = Field(default=10, ge=0)
    RPD_LIMIT: int = Field(default=0, ge=0)
    # After a 429 from the provider, skip the model for this many seconds.
    COOLDOWN_S: float = Field(default=60.0, ge=0)

    # Seconds a model result is reused for the same answers (result page, QR summary
    # scanned later by staff, saving the screening), so they all show the same estimate.
    # In memory: a redeploy clears it. 0 = no reuse.
    CACHE_TTL_S: float = Field(default=86_400.0, ge=0)
    # Flows the model scores. The others always use the rules. Comma-separated.
    FLOWS: str = "infection,chronic"

    # Drug recognition (Q6 free text → drug classes). Needs a model; off = keywords only.
    DRUGS_ENABLED: bool = True

    LITERATURE_DIR: Path = DATA_DIR
    # JSON lines, one per scoring. Empty = write to the "app.triage.ai" logger instead.
    LOG_PATH: Path | None = None
    # Patient facts (option texts, age, sex, province; never name or free text) in the log.
    LOG_FACTS: bool = True

    def flows(self) -> set[str]:
        return {f.strip() for f in self.FLOWS.split(",") if f.strip()}
