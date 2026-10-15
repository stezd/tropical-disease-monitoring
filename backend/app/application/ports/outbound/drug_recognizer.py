"""Outbound port: turn the patient's free-text drug answer into drug classes."""

from typing import Protocol


class DrugRecognizer(Protocol):
    """Finds drug classes (e.g. "nsaid", "acei") in free text.

    Must never raise and must stay within its own time budget: on any trouble it
    returns an empty set, and the keyword rules in advice.json still apply.
    """

    def classes(self, text: str, flow_id: str) -> frozenset[str]: ...
