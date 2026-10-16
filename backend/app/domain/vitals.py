"""Labels for measured blood pressure and blood glucose (DR decisions, 2026-10-15).

Used by the summary (QR page) and the Gemma4 facts. Labels only: they do not change
scores or routes. The route rule for systolic > 160 mmHg lives in route_policy and the
weights (`bp_upgrade_above`).

Perlu OK DR: the label texts below ("normal", "meningkat", "tinggi", "sangat tinggi").
"""

from typing import Literal

BpCategory = Literal["normal", "meningkat", "tinggi", "sangat tinggi"]

# Gula darah sewaktu (GDS): from this value it is "tinggi". DR 2026-10-15.
GLUCOSE_HIGH_FROM = 200.0


def bp_category(sys: int, dia: int) -> BpCategory:
    """Blood pressure category.

    normal: systolic ≤ 120 · meningkat: 120 < systolic < 140 and diastolic < 90 ·
    tinggi: systolic ≥ 140 or diastolic ≥ 90 · sangat tinggi: systolic > 160.
    """
    if sys > 160:
        return "sangat tinggi"
    if sys >= 140 or dia >= 90:
        return "tinggi"
    if sys > 120:
        return "meningkat"
    return "normal"


def glucose_high(glucose: float | None) -> bool:
    return glucose is not None and glucose >= GLUCOSE_HIGH_FROM


def glucose_note(glucose: float) -> str:
    """Suffix after the value, e.g. " (≥ 200, tinggi)". Empty below the cut-off."""
    return f" (≥ {GLUCOSE_HIGH_FROM:g}, tinggi)" if glucose_high(glucose) else ""
