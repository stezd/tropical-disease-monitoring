"""Outbound port: validated quiz content, looked up by flow id."""

from typing import Protocol

from app.domain.triage_content import FlowContent

# Flows the app knows about, in display order. Anything else is a caller bug.
FLOW_IDS = ("infection", "chronic")


class ContentRepository(Protocol):
    """Reads the quiz content the scoring and advice code works on."""

    def get(self, flow_id: str) -> FlowContent:
        """Validated content for a flow.

        Raises KeyError if flow_id is not in FLOW_IDS.
        """
        ...
