"""Call the real model once per case and mode, and print what came back.

    cd backend
    TRIAGE_AI_API_KEY=... python scripts/ai_smoke.py            # both modes
    TRIAGE_AI_API_KEY=... python scripts/ai_smoke.py single     # one mode

Uses about 1 request per case in single mode and 3 to 6 in per_candidate mode, so it
stays well inside the free tier. A line with engine=rules means the model was not used;
`reason` says why (model_off = no key, error = HTTP 4xx, e.g. a schema the API refused).
"""

import sys
from typing import Any

from app.domain.answers import Answers
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine
from app.triage.ai.llm import make_client
from app.triage.content import get_content

CASES: dict[str, tuple[str, dict[str, Any]]] = {
    "malaria (Format-MedGemma)": (
        "infection",
        {
            "who": "self",
            "age": 22,
            "sex": "L",
            "red_flags": ["none"],
            "complaint": "A",
            "pattern": "malaria",
            "companion": ["malaria"],
            "eco": ["timur"],
            "province": "Papua",
            "no_thermo": True,
            "vital_proxy": ["menggigil"],
            "nutrition_proxy": "longgar",
            "body": ["head"],
            "pain": 4,
        },
    ),
    "amebiasis vs diare": (
        "infection",
        {
            "age": 30,
            "sex": "P",
            "pregnant": False,
            "red_flags": ["none"],
            "complaint": "C",
            "pattern": "amoeba",
            "eco": ["none"],
            "temp": 37.8,
            "nutrition_proxy": "normal",
            "body": ["low"],
            "pain": 6,
        },
    ),
    "kronis: gout": (
        "chronic",
        {
            "age": 55,
            "sex": "L",
            "red_flags": ["none"],
            "complaint": "H",
            "pattern": "gout",
            "eco": ["metabolik"],
            "bp_sys": 145,
            "bp_dia": 90,
            "height_cm": 168,
            "weight_kg": 82,
        },
    ),
}


def main() -> None:
    modes = sys.argv[1:] or ["single", "per_candidate"]
    for mode in modes:
        s = AISettings(MODE=mode)  # type: ignore[arg-type]
        eng = AIEngine(s, make_client(s))
        sys.stdout.write(f"\n== mode={mode} model={eng.model}\n")
        for name, (flow_id, raw) in CASES.items():
            b = eng.score(Answers.model_validate(raw), get_content(flow_id))
            m = b.meta
            assert m is not None
            top = ", ".join(f"{r.id} {r.score:.0f}" for r in b.ranked[:3]) or "-"
            sys.stdout.write(
                f"{name:28} engine={m.engine} reason={m.reason} calls={m.calls} "
                f"{m.latency_ms} ms | {top}\n"
            )
            for d, note in list(m.notes.items())[:3]:
                sys.stdout.write(f"{'':28}   {d}: {note}\n")


if __name__ == "__main__":
    main()
