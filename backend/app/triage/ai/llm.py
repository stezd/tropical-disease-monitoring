"""Model clients. One method: `generate_json(system, user, schema, timeout)`.

The scorer never knows which provider it talks to. Add a provider by writing a class
with the same method and returning it from `make_client`.
"""

import time
from dataclasses import dataclass
from typing import Any, Protocol

import httpx

from app.triage.ai.config import AISettings

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


class LLMError(Exception):
    """Any failure talking to the model. `kind` goes to the log as the fallback reason."""

    kind = "error"
    retryable = False


class LLMNetworkError(LLMError):
    kind = "network"
    retryable = True


class LLMServerError(LLMError):
    kind = "server_error"
    retryable = True


class LLMTimeout(LLMError):
    kind = "timeout"


class LLMRateLimited(LLMError):
    kind = "rate_limited"


class LLMBadResponse(LLMError):
    """Empty, blocked, truncated, or not the JSON we asked for."""

    kind = "bad_response"


@dataclass
class LLMReply:
    text: str
    model: str
    latency_ms: int
    input_tokens: int | None = None
    output_tokens: int | None = None


class LLMClient(Protocol):
    model: str

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply: ...


def _short(text: str, n: int = 300) -> str:
    return text if len(text) <= n else text[:n] + "…"


def _raise_for_status(r: httpx.Response) -> None:
    if r.status_code == 429:
        raise LLMRateLimited(_short(r.text))
    if r.status_code >= 500:
        raise LLMServerError(f"HTTP {r.status_code}: {_short(r.text)}")
    if r.status_code >= 400:
        raise LLMError(f"HTTP {r.status_code}: {_short(r.text)}")


def _post(
    http: httpx.Client,
    url: str,
    body: dict[str, Any],
    headers: dict[str, str],
    t: float,
) -> tuple[dict[str, Any], int]:
    start = time.monotonic()
    try:
        r = http.post(url, json=body, headers=headers, timeout=t)
    except httpx.TimeoutException as e:
        raise LLMTimeout(str(e) or "timeout") from e
    except httpx.HTTPError as e:
        raise LLMNetworkError(str(e)) from e
    latency = int((time.monotonic() - start) * 1000)
    _raise_for_status(r)
    try:
        data = r.json()
    except ValueError as e:
        raise LLMBadResponse("response is not JSON") from e
    if not isinstance(data, dict):
        raise LLMBadResponse("response is not a JSON object")
    return data, latency


class GeminiClient:
    """Google AI Studio (Gemini API), `models.generateContent` with a JSON Schema."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str = "",
        thinking_level: str = "",
        temperature: float | None = None,
        http: httpx.Client | None = None,
        fallback_model: str = "",
    ) -> None:
        self.model = model
        # Tried once when the main model answers 503 (busy) or 429 (its quota is used
        # up). Each Gemini model has its own free-tier quota.
        self.fallback_model = fallback_model if fallback_model != model else ""
        self._key = api_key
        self._base = (base_url or GEMINI_BASE_URL).rstrip("/")
        self._thinking = thinking_level
        self._temperature = temperature
        self._http = http or httpx.Client()

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        start = time.monotonic()
        try:
            return self._generate(self.model, system, user, schema, timeout)
        except LLMServerError, LLMRateLimited:
            left = timeout - (time.monotonic() - start)
            if not self.fallback_model or left < 1.0:
                raise
            return self._generate(self.fallback_model, system, user, schema, left)

    def _generate(
        self,
        model: str,
        system: str,
        user: str,
        schema: dict[str, Any],
        timeout: float,
    ) -> LLMReply:
        config: dict[str, Any] = {
            "responseMimeType": "application/json",
            "responseJsonSchema": schema,
        }
        if self._temperature is not None:
            config["temperature"] = self._temperature
        if self._thinking:
            config["thinkingConfig"] = {"thinkingLevel": self._thinking}
        body = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": config,
        }
        data, latency = _post(
            self._http,
            f"{self._base}/models/{model}:generateContent",
            body,
            {"x-goog-api-key": self._key},
            timeout,
        )
        candidates = data.get("candidates") or []
        if not candidates:
            block = (data.get("promptFeedback") or {}).get(
                "blockReason", "no candidates"
            )
            raise LLMBadResponse(f"blocked: {block}")
        first = candidates[0]
        parts = (first.get("content") or {}).get("parts") or []
        text = "".join(
            p.get("text", "")
            for p in parts
            if isinstance(p, dict) and not p.get("thought")
        ).strip()
        finish = first.get("finishReason", "")
        if not text:
            raise LLMBadResponse(f"empty reply (finishReason={finish})")
        if finish == "MAX_TOKENS":
            raise LLMBadResponse("reply cut off (MAX_TOKENS)")
        usage = data.get("usageMetadata") or {}
        out_tokens = (usage.get("candidatesTokenCount") or 0) + (
            usage.get("thoughtsTokenCount") or 0
        )
        return LLMReply(
            text=text,
            model=str(data.get("modelVersion") or model),
            latency_ms=latency,
            input_tokens=usage.get("promptTokenCount"),
            output_tokens=out_tokens or None,
        )


class OpenAICompatClient:
    """Any server with an OpenAI-style /chat/completions and JSON Schema output,
    e.g. vLLM serving MedGemma (`--guided-decoding-backend` supports json_schema)."""

    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str = "",
        temperature: float | None = None,
        http: httpx.Client | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("TRIAGE_AI_BASE_URL is required for openai_compat")
        self.model = model
        self._base = base_url.rstrip("/")
        self._key = api_key
        self._temperature = temperature
        self._http = http or httpx.Client()

    def generate_json(
        self, system: str, user: str, schema: dict[str, Any], timeout: float
    ) -> LLMReply:
        body: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "triage_output",
                    "schema": schema,
                    "strict": True,
                },
            },
        }
        if self._temperature is not None:
            body["temperature"] = self._temperature
        headers = {"Authorization": f"Bearer {self._key}"} if self._key else {}
        data, latency = _post(
            self._http, f"{self._base}/chat/completions", body, headers, timeout
        )
        try:
            choice = data["choices"][0]
            text = (choice["message"].get("content") or "").strip()
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            raise LLMBadResponse("no choices in reply") from e
        if not text:
            raise LLMBadResponse("empty reply")
        if choice.get("finish_reason") == "length":
            raise LLMBadResponse("reply cut off (length)")
        usage = data.get("usage") or {}
        return LLMReply(
            text=text,
            model=str(data.get("model") or self.model),
            latency_ms=latency,
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
        )


def make_client(s: AISettings) -> LLMClient | None:
    """The configured client, or None when the model is off or has no key."""
    key = s.API_KEY.get_secret_value()
    match s.PROVIDER:
        case "gemini" if key:
            return GeminiClient(
                s.MODEL,
                key,
                s.BASE_URL,
                s.THINKING_LEVEL,
                s.TEMPERATURE,
                fallback_model=s.FALLBACK_MODEL,
            )
        case "openai_compat" if s.BASE_URL:
            return OpenAICompatClient(s.MODEL, s.BASE_URL, key, s.TEMPERATURE)
        case _:
            return None
