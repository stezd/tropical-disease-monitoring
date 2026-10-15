"""Build app/triage/ai/data/<flow>_literature.json from a chunk file. Run offline, once.

    python scripts/build_literature.py --flow infection \
        --chunks app/triage/ai/data/infection_chunks.jsonl

Input: JSON lines with `disease`, `sumber`, `judul_bab`, `halaman`, `teks`
(the output of pemotong_dokumen.ipynb). Diseases not scored in the flow (rabies) are
skipped.

Ranking: BM25 over all chunks, then kept per disease, so the model only ever gets
excerpts about the candidate it is scoring. This is the interim builder. A Colab
notebook with EmbeddingGemma can replace it by writing the same JSON format
(see app/triage/ai/literature.py); the service does not change.
"""

import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from app.triage.ai.config import DATA_DIR
from app.triage.ai.literature import FORMAT_VERSION, option_queries
from app.triage.content import get_content

# Shown to the model as "{sumber} · {judul_bab} · hlm. {halaman}". Fill in the full
# titles approved by DR for 54, 20, and 57.
SOURCE_TITLES = {
    "29": "Kemenkes RI · KMK HK.01.07/MENKES/1186/2022 (PPK Dokter di FKTP) · 2022",
    "54": "Dokumen 54 (Skistosomiasis)",
    "20": "Dokumen 20 (Frambusia)",
    "57": "Dokumen 57 (Chikungunya, laporan kasus)",
}

STOPWORDS = set(
    """
    dan atau yang di ke dari pada untuk dengan dalam ini itu adalah akan tidak juga
    oleh sebagai karena bila jika saat setelah serta lebih sangat tiap ada tanpa belum
    hari kali seperti terasa terutama walau bisa dapat secara antara
    """.split()
)
K1, B = 1.2, 0.75
TOP_PER_DISEASE = 5


def tokens(text: str) -> list[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if len(w) > 2 and w not in STOPWORDS]


class BM25:
    def __init__(self, docs: list[list[str]]) -> None:
        self.docs = [Counter(d) for d in docs]
        self.lens = [len(d) for d in docs]
        self.avg = sum(self.lens) / max(1, len(docs))
        n = len(docs)
        df = Counter(w for d in self.docs for w in d)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in df.items()}

    def score(self, query: list[str], i: int) -> float:
        d, length = self.docs[i], self.lens[i]
        s = 0.0
        for w in set(query):
            f = d.get(w, 0)
            if f:
                s += (
                    self.idf[w]
                    * f
                    * (K1 + 1)
                    / (f + K1 * (1 - B + B * length / self.avg))
                )
        return s


def build(flow_id: str, rows: list[dict[str, object]]) -> dict[str, object]:
    content = get_content(flow_id)
    scored = set(content.scored_diseases)
    rows = [r for r in rows if r["disease"] in scored]
    chunks = {
        f"c{i:03d}": {
            "disease": str(r["disease"]),
            "citation": f"{SOURCE_TITLES.get(str(r['sumber']), f'Dokumen {r["sumber"]}')}"
            f" · {r['judul_bab']} · hlm. {r['halaman']}",
            "text": " ".join(str(r["teks"]).split()),
        }
        for i, r in enumerate(rows, start=1)
    }
    ids = list(chunks)
    bm25 = BM25([tokens(c["text"]) for c in chunks.values()])
    by_disease: dict[str, list[int]] = {}
    for i, cid in enumerate(ids):
        by_disease.setdefault(chunks[cid]["disease"], []).append(i)

    def ranked(query: str, disease: str) -> list[list[object]]:
        q = tokens(query)
        hits = [(ids[i], bm25.score(q, i)) for i in by_disease.get(disease, [])]
        hits = [(c, round(s, 3)) for c, s in hits if s > 0]
        hits.sort(key=lambda h: h[1], reverse=True)
        return [[c, s] for c, s in hits[:TOP_PER_DISEASE]]

    options: dict[str, dict[str, list[list[object]]]] = {}
    for key, query in option_queries(content).items():
        per = {d: r for d in sorted(by_disease) if (r := ranked(query, d))}
        if per:
            options[key] = per
    # No answer points anywhere: the disease's own name and the usual PPK headings.
    default = {
        d: [
            str(c)
            for c, _ in ranked(
                f"{content.diseases[d].name} hasil anamnesis gejala keluhan", d
            )
        ]
        or [ids[i] for i in by_disease[d][:TOP_PER_DISEASE]]
        for d in sorted(by_disease)
    }
    missing = sorted(scored - set(by_disease))
    if missing:
        sys.stderr.write(f"warning: no chunks for {', '.join(missing)}\n")
    return {
        "version": FORMAT_VERSION,
        "flow_id": flow_id,
        "method": "bm25-v1",
        "built_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "chunks": chunks,
        "default": default,
        "options": options,
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--flow", required=True, choices=["infection", "chronic"])
    p.add_argument("--chunks", required=True, type=Path)
    p.add_argument("--out", type=Path)
    args = p.parse_args()
    rows = [
        json.loads(line)
        for line in args.chunks.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    data = build(args.flow, rows)
    out = args.out or DATA_DIR / f"{args.flow}_literature.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    n_chunks = len(data["chunks"])  # type: ignore[arg-type]
    n_keys = len(data["options"])  # type: ignore[arg-type]
    sys.stdout.write(f"{out}: {n_chunks} chunks, {n_keys} option keys\n")


if __name__ == "__main__":
    main()
