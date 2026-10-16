"""Does google/embeddinggemma-2 understand the Indonesian cards? Run before trusting it.

    uv run --with sentence-transformers python scripts/embed_langcheck.py \
        --chunks app/triage/ai/data/infection_chunks.jsonl

The model card says "100+ languages" and never names Indonesian, so this measures it on
the real corpus. Each query is searched against ALL chunks (no per-disease filter, which
is harder than what the app does) and scored on whether the top hits belong to the
right disease. The same queries are run through plain BM25 as a reference, and a few
sentence pairs check Indonesian against English and against unrelated text.

Registers per disease: clinical Indonesian, patient wording (how people actually talk),
the real quiz option text from flow.json, and English (only a sanity check, the app is
Indonesian). Verdict is printed at the end; adjust PASS_* if DR wants a stricter bar.
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
from build_literature import DOC_PREFIX, QUERY_PREFIX, load_embedder


def say(text: str = "") -> None:
    sys.stdout.write(text + "\n")


# (disease, register, query)
QUERIES: list[tuple[str, str, str]] = [
    (
        "malaria",
        "klinis",
        "demam menggigil berselang dengan keringat banyak, tinggal di daerah endemis malaria",
    ),
    ("malaria", "awam", "badan panas dingin gemetar lalu keringetan, habis dari Papua"),
    ("malaria", "opsi", "Menggigil berulang tiap 2–3 hari"),
    ("malaria", "opsi", "Keringat dingin deras & pucat usai demam"),
    ("malaria", "english", "recurrent fever with shaking chills and sweating"),
    (
        "dbd",
        "klinis",
        "demam tinggi mendadak 2 sampai 7 hari, nyeri retroorbital, ruam petekie, trombosit menurun",
    ),
    (
        "dbd",
        "awam",
        "panas tinggi tiba-tiba, sakit di belakang mata, ada bintik merah, makin lemas",
    ),
    ("dbd", "opsi", "Tinggi mendadak, turun hari ke-3/4, tapi makin lemas"),
    ("dbd", "opsi", "Nyeri belakang mata / sakit kepala hebat"),
    ("dbd", "english", "sudden high fever with pain behind the eyes and petechiae"),
    (
        "kusta",
        "klinis",
        "bercak hipopigmentasi atau eritematosa dengan hilangnya sensasi dan penebalan saraf tepi",
    ),
    (
        "kusta",
        "awam",
        "ada bercak di kulit yang kebas, tidak gatal, tidak sakit kalau dicubit",
    ),
    ("kusta", "opsi", "Bercak kulit yang mati rasa"),
    ("kusta", "english", "skin patch with loss of sensation and thickened nerves"),
]
PAIRS: list[tuple[str, str, str]] = [
    ("sama arti ID/EN", "demam menggigil berulang", "recurrent fever with chills"),
    (
        "sama arti ID/ID",
        "bercak kulit mati rasa",
        "lesi kulit dengan hilangnya sensasi raba",
    ),
    ("beda topik", "bercak kulit mati rasa", "harga beras naik di pasar"),
]
PASS_TOP5 = 0.60  # mean share of the top 5 hits that are the right disease (Indonesian)
PASS_TOP1 = 0.75  # share of Indonesian queries whose #1 hit is the right disease
ALIAS = {"dbd": {"dbd"}, "malaria": {"malaria"}, "kusta": {"kusta"}}


def tokens(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2]


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.2, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs]
        self.len = [len(d) for d in docs]
        self.avg = sum(self.len) / len(docs)
        df = Counter(w for t in self.tf for w in t)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(len(self.tf))
        for i, (t, length) in enumerate(zip(self.tf, self.len, strict=True)):
            for w in set(query):
                if f := t.get(w, 0):
                    out[i] += (
                        self.idf[w]
                        * f
                        * (self.k1 + 1)
                        / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
                    )
        return out


def judge(
    sims: np.ndarray, labels: list[str], want: str
) -> tuple[int, float, int | None]:
    order = np.argsort(-sims, kind="stable")
    top = [labels[i] for i in order[:5]]
    first = next((r + 1 for r, i in enumerate(order) if labels[i] in ALIAS[want]), None)
    return int(top[0] in ALIAS[want]), sum(t in ALIAS[want] for t in top) / 5, first


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--chunks", required=True, type=Path)
    args = ap.parse_args()
    rows = [
        json.loads(x)
        for x in args.chunks.read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    labels = [r["disease"] for r in rows]
    texts = [" ".join(r["teks"].split()) for r in rows]

    embed = load_embedder()
    docs = embed(texts, "doc")
    qvec = embed([q for _, _, q in QUERIES], "query")
    bm25 = BM25([tokens(t) for t in texts])

    say(f"{len(rows)} chunks. prefix: {QUERY_PREFIX!r} / {DOC_PREFIX!r}\n")
    say(
        f"{'penyakit':8} {'daftar':8} {'emb@1':>5} {'emb@5':>6} {'rank':>5} | {'bm25@1':>6} {'bm25@5':>7}  query"
    )
    agg: dict[str, list[tuple[float, float, float, float]]] = {}
    for (d, reg, q), v in zip(QUERIES, qvec, strict=True):
        e1, e5, rank = judge(docs @ v, labels, d)
        b1, b5, _ = judge(bm25.scores(tokens(q)), labels, d)
        agg.setdefault(reg, []).append((e1, e5, b1, b5))
        say(
            f"{d:8} {reg:8} {e1:>5} {e5:>6.1f} {rank or '-':>5} | {b1:>6} {b5:>7.1f}  {q[:48]}"
        )

    say("\nrata-rata per daftar (emb@1, emb@5, bm25@1, bm25@5)")
    for reg, vals in agg.items():
        m = np.mean(vals, axis=0)
        say(f"  {reg:8} " + "  ".join(f"{x:.2f}" for x in m))

    say("\npasangan kalimat (cosine, makin tinggi makin mirip)")
    for name, a, b in PAIRS:
        va, vb = embed([a], "query")[0], embed([b], "query")[0]
        say(f"  {name:16} {float(va @ vb):.3f}  | {a} <> {b}")

    ind = [x for r, v in agg.items() if r != "english" for x in v]
    top1 = float(np.mean([x[0] for x in ind]))
    top5 = float(np.mean([x[1] for x in ind]))
    ok = top1 >= PASS_TOP1 and top5 >= PASS_TOP5
    say(
        f"\nIndonesia: emb@1={top1:.2f} (batas {PASS_TOP1}), emb@5={top5:.2f} (batas {PASS_TOP5})"
        f" -> {'LOLOS' if ok else 'TIDAK LOLOS: jangan pakai embedding sebelum diperiksa'}"
    )
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
