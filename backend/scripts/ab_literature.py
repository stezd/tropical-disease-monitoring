"""A/B/C: rules vs AI without literature vs AI with the embedding literature.

    cd backend
    TRIAGE_AI_API_KEY=... python scripts/ab_literature.py            # single mode
    TRIAGE_AI_API_KEY=... python scripts/ab_literature.py per_candidate

Cases: every quiz pattern option that names one disease (19) as a minimal answer set,
plus the infection cases of ai_smoke.py, whose expected disease is the one in `pattern`.
This measures "does the arm put the intended disease first", not clinical truth: the
real judgement is DR's, on the Swagger comparison in the README. Spends 2 model calls
per case in single mode (about 3 to 6 each in per_candidate), paced by
TRIAGE_AI_RPM_LIMIT.
"""

import sys
import time
from dataclasses import dataclass
from typing import Any

from app.domain.answers import Answers
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine
from app.triage.ai.literature import option_queries
from app.triage.ai.llm import make_client
from app.triage.content import get_content
from app.triage.scoring import RuleEngine


@dataclass
class Run:
    top: list[str]
    engine: str
    reason: str | None
    latency_ms: int
    cited: int


def cases() -> dict[str, tuple[dict[str, Any], str]]:
    out: dict[str, tuple[dict[str, Any], str]] = {}
    for key in option_queries(get_content("infection")):
        kind, *rest = key.split(":")
        if kind == "pattern":
            cluster, disease = rest
            out[f"{cluster}/{disease}"] = (
                {
                    "age": 30,
                    "sex": "L",
                    "red_flags": ["none"],
                    "complaint": cluster,
                    "pattern": disease,
                    "no_thermo": True,
                },
                disease,
            )
    from ai_smoke import CASES  # same folder: scripts/

    for name, (flow, raw) in CASES.items():
        if flow == "infection" and raw.get("pattern"):
            out[name] = (raw, str(raw["pattern"]))
    return out


def run_rules(raw: dict[str, Any]) -> Run:
    b = RuleEngine().score(Answers.model_validate(raw), get_content("infection"))
    return Run([r.id for r in b.ranked], "rules", None, 0, 0)


def run_ai(eng: AIEngine, raw: dict[str, Any]) -> Run:
    b = eng.score(Answers.model_validate(raw), get_content("infection"))
    m = b.meta
    assert m is not None
    cited = sum(len(v) for v in m.sources.values())
    return Run([r.id for r in b.ranked], m.engine, m.reason, m.latency_ms, cited)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "single"
    with_rag = AISettings(MODE=mode)  # type: ignore[arg-type]
    no_rag = AISettings(
        MODE=mode, SOURCES_PER_CANDIDATE=0, SOURCES_PER_CANDIDATE_SINGLE=0
    )  # type: ignore[arg-type]
    arms = {
        "rules": None,
        "AI tanpa RAG": AIEngine(no_rag, make_client(no_rag)),
        "AI + RAG": AIEngine(with_rag, make_client(with_rag)),
    }
    pause = 60 / with_rag.RPM_LIMIT if with_rag.RPM_LIMIT else 0
    stats: dict[str, dict[str, float]] = {
        a: {"n": 0, "top1": 0, "top3": 0, "fallback": 0, "ms": 0, "cited": 0}
        for a in arms
    }
    sys.stdout.write(
        f"mode={mode} model={with_rag.MODEL}\n\n{'kasus':24}{'harapan':11}"
        + "".join(f"{a:22}" for a in arms)
        + "\n"
    )
    for name, (raw, want) in cases().items():
        row = f"{name:24}{want:11}"
        for arm, eng in arms.items():
            r = run_rules(raw) if eng is None else run_ai(eng, raw)
            if eng is not None and r.engine == "ai":
                time.sleep(pause * max(1, 1 if mode == "single" else 4))
            s = stats[arm]
            s["n"] += 1
            s["top1"] += r.top[:1] == [want]
            s["top3"] += want in r.top[:3]
            s["fallback"] += r.engine != "ai" and eng is not None
            s["ms"] += r.latency_ms
            s["cited"] += r.cited
            row += (
                f"{','.join(r.top[:3]) + ('*' if eng and r.engine != 'ai' else ''):22}"
            )
        sys.stdout.write(row + "\n")
    sys.stdout.write("\n(* = model tidak dipakai, hasil dari aturan)\n\n")
    sys.stdout.write(
        f"{'lengan':14}{'n':>4}{'top1':>7}{'top3':>7}{'fallback':>10}{'ms/kasus':>10}{'sumber':>8}\n"
    )
    for arm, s in stats.items():
        n = s["n"] or 1
        sys.stdout.write(
            f"{arm:14}{int(s['n']):4}{s['top1'] / n:7.2f}{s['top3'] / n:7.2f}"
            f"{int(s['fallback']):10}{s['ms'] / n:10.0f}{int(s['cited']):8}\n"
        )


if __name__ == "__main__":
    main()
