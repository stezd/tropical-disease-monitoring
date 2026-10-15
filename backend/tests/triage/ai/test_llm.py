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
    c = OpenAICompatClient("medgemma", "http://gpu:8000/v1", "tok", http=http)
    r = c.generate_json("S", "U", SCHEMA, 3)
    assert r.text == '{"score": 1}' and r.output_tokens == 3
    assert seen["auth"] == "Bearer tok"
    assert seen["body"]["response_format"]["json_schema"]["schema"] == SCHEMA


def test_make_client_from_settings() -> None:
    assert make_client(AISettings(API_KEY="")) is None
    assert make_client(AISettings(PROVIDER="off", API_KEY="k")) is None
    assert isinstance(make_client(AISettings(API_KEY="k")), GeminiClient)
    c = make_client(AISettings(PROVIDER="openai_compat", BASE_URL="http://x/v1"))
    assert isinstance(c, OpenAICompatClient)
