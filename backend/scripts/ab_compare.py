"""Same cases through three arms, so the RAG change is judged on numbers, not feel.

    cd backend
    TRIAGE_AI_API_KEY=... python scripts/ab_compare.py [--repeat 2] [--out ab.jsonl]

Arms:  rules      RuleEngine, no model.
       ai_no_rag  the model with no literature (0 excerpts per candidate).
       ai_rag     the model with the excerpts from infection_literature.json.

Each arm has its own engine and the result cache is off, so nothing is shared (the
cache key ignores settings: reusing one process for two arms would return the first
arm's answer). `expect` is the author's reading of each case, not a DR verdict: have DR
confirm the list before quoting the numbers. Without an API key the AI arms fall back
to rules and the script says so instead of reporting fake wins.
"""

import argparse
import json
import logging
import sys
import time
from typing import Any

from app.domain.answers import Answers
from app.triage.ai.config import AISettings
from app.triage.ai.engine import AIEngine
from app.triage.ai.llm import make_client
from app.triage.content import get_content
from app.triage.scoring import RuleEngine


def say(text: str = "") -> None:
    sys.stdout.write(text + "\n")


BASE: dict[str, Any] = {
    "age": 30,
    "sex": "L",
    "red_flags": ["none"],
    "no_thermo": True,
    "nutrition_proxy": "normal",
    "pain": 3,
}


def case(expect: set[str], **kw: Any) -> tuple[set[str], dict[str, Any]]:
    return expect, {**BASE, **kw}


CASES: dict[str, tuple[set[str], dict[str, Any]]] = {
    "malaria": case(
        {"malaria"},
        complaint="A",
        pattern="malaria",
        companion=["malaria"],
        eco=["timur"],
        vital_proxy=["menggigil"],
        province="Papua",
        body=["head"],
    ),
    "dbd": case(
        {"dbd"},
        complaint="A",
        pattern="dbd",
        companion=["dbd"],
        no_thermo=False,
        temp=39.4,
        body=["head"],
    ),
    "chik": case(
        {"chik"},
        complaint="A",
        pattern="chik",
        companion=["chik"],
        no_thermo=False,
        temp=38.5,
        body=["knee_l", "knee_r"],
    ),
    "lepto": case(
        {"lepto"}, complaint="A", pattern="lepto", eco=["banjir"], body=["calf_l"]
    ),
    "skisto": case(
        {"skisto"},
        complaint="A",
        pattern="skisto",
        eco=["danau"],
        province="Sulawesi Tengah",
        body=["low"],
    ),
    "tbc": case(
        {"tbc"}, complaint="B", pattern="tbc", companion=["bb", "kms"], eco=["kontak"]
    ),
    "ispa": case({"ispa"}, complaint="B", pattern="ispa", companion=["none"]),
    "amoeba": case(
        {"amoeba"},
        complaint="C",
        pattern="amoeba",
        eco=["none"],
        no_thermo=False,
        temp=37.8,
        body=["low"],
    ),
    "tifoid": case(
        {"tifoid"},
        complaint="C",
        pattern="tifoid",
        no_thermo=False,
        temp=39.0,
        body=["low"],
    ),
    "kusta": case({"kusta"}, complaint="D", pattern="kusta", companion=["none"]),
    "frambusia": case(
        {"frambusia"}, complaint="D", pattern="frambusia", eco=["timur"], province="NTT"
    ),
    "filaria": case({"filaria"}, complaint="E", pattern="filaria", eco=["none"]),
    # Pattern question answered "none": the rules have only the cluster and side
    # answers to go on, which is where the model and the literature can matter.
    "dbd tanpa pola": case(
        {"dbd"},
        complaint="A",
        pattern="none",
        companion=["dbd"],
        no_thermo=False,
        temp=39.1,
        body=["head"],
    ),
    "chik tanpa pola": case(
        {"chik"},
        complaint="A",
        pattern="none",
        companion=["chik"],
        no_thermo=False,
        temp=38.2,
        body=["knee_l", "knee_r"],
    ),
    "malaria tanpa pola": case(
        {"malaria"},
        complaint="A",
        pattern="none",
        companion=["malaria"],
        eco=["timur"],
        vital_proxy=["menggigil"],
        province="Papua",
    ),
    "tbc tanpa pola": case(
        {"tbc"}, complaint="B", pattern="none", companion=["bb", "kms"], eco=["kontak"]
    ),
}
ARMS = ("rules", "ai_no_rag", "ai_rag")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repeat", type=int, default=1, help="model runs per case and arm")
    ap.add_argument("--out", help="write every run as JSON lines")
    ap.add_argument("--mode", choices=["single", "per_candidate"], default="single")
    args = ap.parse_args()
    logging.getLogger("app.triage.ai").setLevel(logging.WARNING)

    content = get_content("infection")
    rules = RuleEngine()
    s_base = {"MODE": args.mode, "CACHE_TTL_S": 0}
    s_no = AISettings(**s_base, SOURCES_PER_CANDIDATE=0, SOURCES_PER_CANDIDATE_SINGLE=0)  # type: ignore[arg-type]
    s_rag = AISettings(**s_base)  # type: ignore[arg-type]
    engines = {
        "ai_no_rag": AIEngine(s_no, make_client(s_no)),
        "ai_rag": AIEngine(s_rag, make_client(s_rag)),
    }
    pause = 60 / s_rag.RPM_LIMIT + 0.5 if s_rag.RPM_LIMIT else 0

    runs: list[dict[str, Any]] = []
    for name, (expect, raw) in CASES.items():
        a = Answers.model_validate(raw)
        b = rules.score(a, content)
        runs.append(
            {
                "case": name,
                "arm": "rules",
                "expect": sorted(expect),
                "ranked": [r.id for r in b.ranked],
                "engine": "rules",
            }
        )
        for arm, eng in engines.items():
            for _ in range(args.repeat):
                out = eng.score(a, content)
                m = out.meta
                assert m is not None
                runs.append(
                    {
                        "case": name,
                        "arm": arm,
                        "expect": sorted(expect),
                        "ranked": [r.id for r in out.ranked],
                        "engine": m.engine,
                        "reason": m.reason,
                        "calls": m.calls,
                        "latency_ms": m.latency_ms,
                        "sources": m.sources,
                        "notes": m.notes,
                    }
                )
                if m.calls and pause:
                    time.sleep(pause)

    def hit(r: dict[str, Any], k: int) -> bool:
        return bool(set(r["ranked"][:k]) & set(r["expect"]))

    say(f"{'kasus':20} {'harapan':10} " + " ".join(f"{a:>14}" for a in ARMS))
    for name in CASES:
        cells = []
        for arm in ARMS:
            rs = [r for r in runs if r["case"] == name and r["arm"] == arm]
            cells.append(
                "/".join(
                    (r["ranked"][:1] or ["-"])[0]
                    + ("*" if r["engine"] != "ai" and arm != "rules" else "")
                    for r in rs
                )
            )
        say(
            f"{name:20} {','.join(CASES[name][0]):10} "
            + " ".join(f"{c:>14}" for c in cells)
        )
    say("\n* = model tidak dipakai (fallback), hasilnya dari aturan\n")
    for arm in ARMS:
        rs = [r for r in runs if r["arm"] == arm]
        used = [r for r in rs if r["engine"] == ("rules" if arm == "rules" else "ai")]
        lat = sorted(r.get("latency_ms", 0) for r in used)
        say(
            f"{arm:10} n={len(rs):2} model dipakai={len(used):2} "
            f"top1={sum(hit(r, 1) for r in rs) / len(rs):.2f} top3={sum(hit(r, 3) for r in rs) / len(rs):.2f}"
            + (f" median={lat[len(lat) // 2]} ms" if arm != "rules" and lat else "")
        )
    if any(r["engine"] != "ai" for r in runs if r["arm"] != "rules"):
        say("\nPERINGATAN: ada panggilan yang jatuh ke aturan. Angka arm AI belum sah.")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in runs)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
