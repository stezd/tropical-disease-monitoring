import json
from typing import Any

import httpx
import pytest

from app.triage.ai.config import AISettings
from app.triage.ai.llm import (
    GeminiClient,
    LLMBadResponse,
    LLMError,
    LLMNetworkError,
    LLMRateLimited,
    LLMServerError,
    LLMTimeout,
    OpenAICompatClient,
    make_client,
)

SCHEMA = {"type": "object", "properties": {"score": {"type": "integer"}}}


def gemini(handler: Any, **kw: Any) -> GeminiClient:
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return GeminiClient("gemini-x", "KEY", http=http, **kw)


def test_gemini_request_and_reply() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["url"] = str(req.url)
        seen["key"] = req.headers["x-goog-api-key"]
        seen["body"] = json.loads(req.content)
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "thinking...", "thought": True},
                                {"text": '{"score": 7}'},
                            ]
                        },
                        "finishReason": "STOP",
                    }
                ],
                "usageMetadata": {
                    "promptTokenCount": 120,
                    "candidatesTokenCount": 8,
                    "thoughtsTokenCount": 30,
                },
                "modelVersion": "gemini-x-001",
            },
        )

    r = gemini(handler, thinking_level="low").generate_json("SYS", "USER", SCHEMA, 3)
    assert r.text == '{"score": 7}' and r.model == "gemini-x-001"
    assert (r.input_tokens, r.output_tokens) == (120, 38)
    assert seen["url"].endswith("/v1beta/models/gemini-x:generateContent")
    assert seen["key"] == "KEY" and "KEY" not in seen["url"]
    cfg = seen["body"]["generationConfig"]
    assert cfg["responseMimeType"] == "application/json"
    assert cfg["responseJsonSchema"] == SCHEMA
    assert cfg["thinkingConfig"] == {"thinkingLevel": "low"}
    assert seen["body"]["systemInstruction"]["parts"][0]["text"] == "SYS"


@pytest.mark.parametrize(
    ("response", "error"),
    [
        (httpx.Response(429, text="quota"), LLMRateLimited),
        (httpx.Response(503, text="busy"), LLMServerError),
        (httpx.Response(400, text="bad schema"), LLMError),
        (
            httpx.Response(200, json={"promptFeedback": {"blockReason": "SAFETY"}}),
            LLMBadResponse,
        ),
        (
            httpx.Response(
                200,
                json={
                    "candidates": [
                        {
                            "content": {"parts": [{"text": "{"}]},
                            "finishReason": "MAX_TOKENS",
                        }
                    ]
                },
            ),
            LLMBadResponse,
        ),
        (httpx.Response(200, text="<html>"), LLMBadResponse),
    ],
)
def test_gemini_errors(response: httpx.Response, error: type[Exception]) -> None:
    with pytest.raises(error):
        gemini(lambda _r: response).generate_json("S", "U", SCHEMA, 3)


def test_gemini_timeout_and_network() -> None:
    def timeout(req: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("slow", request=req)

    def down(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("down", request=req)

    with pytest.raises(LLMTimeout):
        gemini(timeout).generate_json("S", "U", SCHEMA, 3)
    with pytest.raises(LLMNetworkError):
        gemini(down).generate_json("S", "U", SCHEMA, 3)


def test_openai_compat() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        seen["auth"] = req.headers.get("authorization")
        seen["session"] = req.headers.get("x-opencode-session")
        seen["ua"] = req.headers.get("user-agent")
        return httpx.Response(
            200,
            json={
                "model": "medgemma",
                "choices": [
                    {"message": {"content": '{"score": 1}'}, "finish_reason": "stop"}
                ],
                "usage": {"prompt_tokens": 9, "completion_tokens": 3},
            },
        )

    http = httpx.Client(transport=httpx.MockTransport(handler))
    c = OpenAICompatClient(
        "medgemma",
        "http://gpu:8000/v1",
        "tok",
        http=http,
        extra_headers={"x-opencode-session": "s1", "User-Agent": "tropicare/1.0"},
    )
    r = c.generate_json("S", "U", SCHEMA, 3)
    assert r.text == '{"score": 1}' and r.output_tokens == 3
    assert seen["auth"] == "Bearer tok"
    assert seen["body"]["response_format"]["json_schema"]["schema"] == SCHEMA
    # Not streaming: SSE is not JSON and would break the parse above.
    assert seen["body"]["stream"] is False
    assert seen["session"] == "s1" and seen["ua"] == "tropicare/1.0"


def test_make_client_from_settings() -> None:
    assert make_client(AISettings(API_KEY="")) is None
    assert make_client(AISettings(PROVIDER="off", API_KEY="k")) is None
    assert isinstance(make_client(AISettings(API_KEY="k")), GeminiClient)
    c = make_client(AISettings(PROVIDER="openai_compat", BASE_URL="http://x/v1"))
    assert isinstance(c, OpenAICompatClient)
    # Identity headers reach the client: OpenCode Go rejects callers without a
    # session id (HTTP 400 MissingSessionID).
    c = make_client(
        AISettings(
            PROVIDER="openai_compat",
            BASE_URL="http://x/v1",
            SESSION_ID="s1",
            USER_AGENT="tropicare/1.0",
        )
    )
    assert c._headers == {"x-opencode-session": "s1", "User-Agent": "tropicare/1.0"}


# Real reply from gemini-3.5-flash-lite (15 Oct 2026), shortened. The text part carries
# a thoughtSignature but no `thought` flag, and there is no thoughtsTokenCount.
REAL_REPLY = {
    "candidates": [
        {
            "content": {
                "parts": [
                    {
                        "text": '{"candidates":[{"id":"malaria","note":"Menggigil berkala, Papua.","score":90,"evidence":["F1"],"sources":[]}]}',
                        "thoughtSignature": "EmAKXgFpFH0T",
                    }
                ],
                "role": "model",
            },
            "finishReason": "STOP",
            "index": 0,
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 47,
        "candidatesTokenCount": 106,
        "totalTokenCount": 153,
    },
    "modelVersion": "gemini-3.5-flash-lite",
}


def test_gemini_real_reply_shape() -> None:
    r = gemini(lambda _r: httpx.Response(200, json=REAL_REPLY)).generate_json(
        "S", "U", SCHEMA, 3
    )
    assert json.loads(r.text)["candidates"][0]["score"] == 90
    assert (r.model, r.input_tokens, r.output_tokens) == (
        "gemini-3.5-flash-lite",
        47,
        106,
    )


@pytest.mark.parametrize("status", [503, 429])
def test_gemini_fallback_model_on_busy_or_quota(status: int) -> None:
    urls: list[str] = []

    def handler(req: httpx.Request) -> httpx.Response:
        urls.append(str(req.url))
        if "gemini-main" in str(req.url):
            return httpx.Response(status, text="busy")
        return httpx.Response(200, json=REAL_REPLY)

    c = gemini(handler, fallback_model="gemini-lite")
    c.model = "gemini-main"
    r = c.generate_json("S", "U", SCHEMA, 3)
    assert r.model == "gemini-3.5-flash-lite"
    assert [u.split("/models/")[1] for u in urls] == [
        "gemini-main:generateContent",
        "gemini-lite:generateContent",
    ]


def test_gemini_no_fallback_on_bad_request() -> None:
    calls: list[str] = []

    def handler(req: httpx.Request) -> httpx.Response:
        calls.append(str(req.url))
        return httpx.Response(400, text="bad schema")

    with pytest.raises(LLMError):
        gemini(handler, fallback_model="gemini-lite").generate_json("S", "U", SCHEMA, 3)
    assert len(calls) == 1


def test_gemini_fallback_also_busy_raises() -> None:
    with pytest.raises(LLMServerError):
        gemini(
            lambda _r: httpx.Response(503, text="busy"), fallback_model="gemini-lite"
        ).generate_json("S", "U", SCHEMA, 3)


def test_make_client_passes_fallback_model() -> None:
    c = make_client(
        AISettings(
            API_KEY="k",
            MODEL="gemini-3.6-flash",
            FALLBACK_MODEL="gemini-3.5-flash-lite",
        )
    )
    assert isinstance(c, GeminiClient)
    assert (c.model, c.fallback_model) == ("gemini-3.6-flash", "gemini-3.5-flash-lite")
    assert AISettings.model_fields["MODEL"].default == "gemini-3.5-flash-lite"


def test_temperature_left_to_the_model_by_default() -> None:
    seen: dict[str, Any] = {}

    def handler(req: httpx.Request) -> httpx.Response:
        seen["body"] = json.loads(req.content)
        return httpx.Response(200, json=REAL_REPLY)

    gemini(handler).generate_json("S", "U", SCHEMA, 3)
    assert "temperature" not in seen["body"]["generationConfig"]
    gemini(handler, temperature=0.2).generate_json("S", "U", SCHEMA, 3)
    assert seen["body"]["generationConfig"]["temperature"] == 0.2
