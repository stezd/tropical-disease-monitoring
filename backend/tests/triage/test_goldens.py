"""Frozen ScoreResult snapshots (wave 1 of the ports-and-adapters strangler).

Each case is a golden JSON produced by the unmodified rule engine. Waves 2 and 3
must keep producing byte-identical output for these inputs.
"""

import json
from pathlib import Path
from typing import Any

import pytest

from app.triage.advice import build_result
from app.triage.content import get_content
from app.triage.schemas import Answers
from app.triage.scoring import RuleEngine

GOLDEN_DIR = Path(__file__).parent / "goldens"

# case name → (flow id, answer kwargs). `taken_at` is never set, so the summary stays deterministic.
# The golden JSON in goldens/<name>.json is the frozen ScoreResult for exactly these answers.
CASES: dict[str, tuple[str, dict[str, Any]]] = {
    "low_score_unknown": (
        "infection",
        {
            "age": 30,
            "complaint": "E",
            "pattern": "none",
            "no_thermo": True,
            "nutrition_proxy": "normal",
        },
    ),
    "high_fever_upgrade": (
        "infection",
        {
            "age": 30,
            "complaint": "B",
            "pattern": "ispa",
            "temp": 39.6,
            "nutrition_proxy": "normal",
        },
    ),
    "systolic_above_160": (
        "infection",
        {
            "age": 50,
            "complaint": "B",
            "pattern": "ispa",
            "temp": 37.0,
            "bp_sys": 170,
            "bp_dia": 100,
            "nutrition_proxy": "normal",
        },
    ),
    "severe_varicella_sign": (
        "infection",
        {
            "age": 9,
            "complaint": "D",
            "pattern": "varicella",
            "companion": ["mata"],
            "temp": 37.8,
            "nutrition_proxy": "normal",
        },
    ),
    "red_flag": (
        "infection",
        {"red_flags": ["napas"], "complaint": "B", "pattern": "ispa"},
    ),
    "no_thermometer_proxy": (
        "infection",
        {
            "age": 30,
            "complaint": "A",
            "pattern": "malaria",
            "no_thermo": True,
            "vital_proxy": ["menggigil", "nadi"],
            "nutrition_proxy": "normal",
        },
    ),
    "drug_popup": (
        "infection",
        {"complaint": "C", "pattern": "amoeba", "drugs": "imodium", "no_thermo": True},
    ),
    "chronic_no_complaint": (
        "chronic",
        {"age": 45, "complaint": "none", "eco": ["rokok", "metabolik"], "no_bp": True},
    ),
}


@pytest.mark.parametrize("name", CASES)
def test_golden(name: str) -> None:
    flow_id, kw = CASES[name]
    content = get_content(flow_id)
    answers = Answers.model_validate({"red_flags": ["none"], **kw})
    actual = build_result(
        content.flow.id, answers, content, RuleEngine().score(answers, content)
    ).model_dump(mode="json")
    expected = json.loads((GOLDEN_DIR / f"{name}.json").read_text(encoding="utf-8"))
    assert actual == expected
