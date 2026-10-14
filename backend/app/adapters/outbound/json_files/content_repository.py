"""Outbound adapter: quiz content read from JSON files on disk.

DR and ST edit app/triage/content/<flow_id>/*.json. CONTENT_DIR is derived from this
file's location, so the adapter does not depend on the shim module.
"""

import json
from functools import cache
from pathlib import Path
from typing import Any

from app.application.ports.outbound.content_repository import (
    FLOW_IDS,
    ContentRepository,
)
from app.domain.triage_content import FlowContent

CONTENT_DIR = Path(__file__).parents[3] / "triage" / "content"


def _read(*parts: str) -> Any:
    return json.loads(CONTENT_DIR.joinpath(*parts).read_text(encoding="utf-8"))


def raw_content(flow_id: str) -> dict[str, Any]:
    """The flow's JSON files as dicts, with the shared red flags merged into the flow."""
    return {
        "flow": {**_read(flow_id, "flow.json"), **_read("red_flags.json")},
        "diseases": _read(flow_id, "diseases.json"),
        "advice": _read(flow_id, "advice.json"),
        "weights": _read(flow_id, "weights.json"),
    }


@cache
def get_content(flow_id: str) -> FlowContent:
    """Return validated content for a flow. Raises KeyError for unknown flows."""
    if flow_id not in FLOW_IDS:
        raise KeyError(flow_id)
    return FlowContent.model_validate(raw_content(flow_id))


class JsonFilesContentRepository(ContentRepository):
    """ContentRepository over the JSON files under app/triage/content."""

    def get(self, flow_id: str) -> FlowContent:
        return get_content(flow_id)
