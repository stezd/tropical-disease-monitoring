"""Does EmbeddingGemma 2 understand Indonesian medical text? Run once before trusting it.

    PYTHONPATH=. uv run --with sentence-transformers --with torch --with pillow python scripts/embedding_probe.py \
        --chunks app/triage/ai/data/infection_chunks.jsonl

The model card says "100+ languages" but gives no Indonesian number, so measure it.
Test 1: each quiz option that names one disease (pattern:*:<disease>, 19 of them) is a
query against ALL cards, with no per-disease filter. Top-1 / top-3 disease accuracy and
the mean reciprocal rank are what to read. The three diseases asked about (malaria,
dbd, kusta) are printed in full. Test 2: the same questions written in English, to see
whether Indonesian is clearly worse than English. Test 3: the gap between a card's own
disease and the best other disease (margin), the number that decides whether summing
scores in for_disease() is safe. Nothing is written to disk.

Reading the result: top-3 of 0.8 or more on Indonesian and no more than 0.15 below
English means the model is usable as is. Clearly worse: keep BM25 for those options or
ask DR for better query wording. This script is a check, not a test: it needs the
model download (about 1 GB).
"""

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from app.triage.ai.literature import option_queries
from app.triage.content import get_content

sys.path.insert(0, str(Path(__file__).parent))
from build_literature import Embedder, load_embedder  # noqa: E402

SHOW = ("malaria", "dbd", "kusta")
# Same meaning as the quiz option, in English. Only for the Indonesian vs English check.
ENGLISH = {
    "dbd": "High fever that drops on day 3 or 4, then weakness (saddleback fever)",
    "chik": "Short fever of 1 to 3 days with a red rash",
    "malaria": "Shaking chills fever that recurs regularly every 2 to 3 days",
    "lepto": "Irregular fever with severe calf pain",
    "skisto": "Persistent fever, abdominal pain, itching after swimming in a lake",
    "ispa": "Cough under 14 days with blocked nose, sneezing, itchy throat",
    "tbc": "Cough lasting more than 2 weeks in a row",
    "amoeba": "Bloody mucous stool with painful straining",
    "tifoid": "Stepwise rising fever, peaking at night, with abdominal pain",
    "hepa": "Tea-coloured urine and right upper abdominal pain",
    "sth": "Swollen belly, thin child, anal itching, worms in stool",
    "scabies": "Severe itching at night between the fingers and skin folds",
    "tinea": "Scaly patches that itch when sweating",
    "campak": "Generalised rash after fever, cough, runny nose, red eyes",
    "varicella": "Fluid-filled blisters spreading over the whole body",
    "kusta": "Skin patch with loss of sensation (numb)",
    "frambusia": "Raised raspberry-like sore that does not heal",
    "filaria": "Swelling for more than 3 months, non-pitting, persists when the leg is raised",
}


def rank_cards(
    qvec: list[float], doc_vecs: list[list[float]], diseases: list[str]
) -> list[tuple[str, float]]:
    scored = [
        (d, math.sumprod(qvec, v)) for d, v in zip(diseases, doc_vecs, strict=True)
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)


def evaluate(
    queries: dict[str, str],
    gold: dict[str, str],
    emb: Embedder,
    doc_vecs: list[list[float]],
    diseases: list[str],
    *,
    verbose: bool,
    texts: list[str],
) -> dict[str, float]:
    keys = list(queries)
    qvecs = emb.queries([queries[k] for k in keys])
    top1 = top3 = rr = 0.0
    margins: list[float] = []
    for key, qv in zip(keys, qvecs, strict=True):
        ranked = rank_cards(qv, doc_vecs, diseases)
        want = gold[key]
        order: list[str] = []
        for d, _ in ranked:
            if d not in order:
                order.append(d)
        pos = order.index(want) + 1 if want in order else len(order) + 1
        top1 += pos == 1
        top3 += pos <= 3
        rr += 1 / pos
        best_own = max(s for d, s in ranked if d == want)
        best_other = max((s for d, s in ranked if d != want), default=0.0)
        margins.append(best_own - best_other)
        if verbose and want in SHOW:
            sys.stdout.write(f"\n[{key}] {queries[key]}\n")
            for i, (d, s) in enumerate(ranked[:5]):
                sys.stdout.write(
                    f"  {i + 1}. {s:.3f} {d:10} {texts[diseases.index(d)][:70]}\n"
                )
    n = len(keys)
    return {
        "n": n,
        "top1": top1 / n,
        "top3": top3 / n,
        "mrr": rr / n,
        "margin": sum(margins) / n,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--chunks", required=True, type=Path)
    args = ap.parse_args()
    rows = [
        json.loads(x)
        for x in args.chunks.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    content = get_content("infection")
    rows = [
        r
        for r in rows
        if r["disease"] in set(content.scored_diseases) and r["teks"].startswith("[")
    ]
    texts = [" ".join(r["teks"].split()) for r in rows]
    diseases = [r["disease"] for r in rows]
    emb = load_embedder()
    doc_vecs = emb.documents(texts)

    id_q = {
        k: v for k, v in option_queries(content).items() if k.startswith("pattern:")
    }
    gold = {k: k.split(":")[2] for k in id_q}
    en_q = {k: ENGLISH[gold[k]] for k in id_q if gold[k] in ENGLISH}

    by_lang = {
        "Indonesia": evaluate(
            id_q, gold, emb, doc_vecs, diseases, verbose=True, texts=texts
        ),
        "Inggris": evaluate(
            en_q, gold, emb, doc_vecs, diseases, verbose=False, texts=texts
        ),
    }
    sys.stdout.write("\nbahasa     n  top1  top3   mrr  margin\n")
    for lang, m in by_lang.items():
        sys.stdout.write(
            f"{lang:9} {int(m['n']):2}  {m['top1']:.2f}  {m['top3']:.2f}  {m['mrr']:.2f}  {m['margin']:+.3f}\n"
        )
    gap = by_lang["Inggris"]["top3"] - by_lang["Indonesia"]["top3"]
    ok = by_lang["Indonesia"]["top3"] >= 0.8 and gap <= 0.15
    sys.stdout.write(
        f"\nselisih top3 Inggris - Indonesia: {gap:+.2f} -> "
        f"{'Indonesia cukup baik' if ok else 'PERIKSA: Indonesia lemah'}\n"
    )
    per: dict[str, list[float]] = defaultdict(list)
    for r in (id_q,):
        for k, qv in zip(r, emb.queries(list(r.values())), strict=True):
            ranked = rank_cards(qv, doc_vecs, diseases)
            per[gold[k]].append(max(s for d, s in ranked if d == gold[k]))
    sys.stdout.write("\nskor kartu terbaik penyakitnya sendiri (cosine):\n")
    for d, v in sorted(per.items()):
        sys.stdout.write(f"  {d:10} {sum(v) / len(v):.3f}\n")


if __name__ == "__main__":
    main()
