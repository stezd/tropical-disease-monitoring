"""Build app/triage/ai/data/<flow>_literature.json from a chunk file. Run offline, once.

    PYTHONPATH=. uv run --with sentence-transformers --with torch python scripts/build_literature.py \
        --flow infection --chunks app/triage/ai/data/infection_chunks.jsonl

Input: JSON lines with `disease`, `sumber`, `judul_bab`, `halaman`, `teks`. Every `teks`
starts with a "[Penyakit · Bagian]" tag. Diseases not scored in the flow (rabies) are
skipped. Cards without the tag are skipped too (see --keep-untagged).

Ranking: google/embeddinggemma-2, text only, float32 on CPU, 768 dimensions, L2
normalised, so cosine similarity = dot product. Queries are the Indonesian option texts
of the quiz ("task: search result | query: ..."), documents are the cards ("title: none
| text: ..."). Scores are kept per disease, so the model only ever gets excerpts about
the candidate it is scoring. The output format is the one in app/triage/ai/literature.py
(plus a "model" key the loader ignores); runtime code does not embed anything.
sentence-transformers and torch are needed for this script only, not by the app.
"""

import argparse
import importlib
import json
import math
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from app.triage.ai.config import DATA_DIR
from app.triage.ai.literature import FORMAT_VERSION, option_queries, section_of
from app.triage.content import get_content

MODEL_ID = "google/embeddinggemma-2"
METHOD = "embedding-v1"
DIMS = 768
QUERY_PREFIX = "task: search result | query: "
DOC_PREFIX = "title: none | text: "
TOP_PER_DISEASE = 5
# Cosine floor. Dense scores are rarely negative, so this only removes noise;
# calibrate it with scripts/embedding_probe.py before raising it.
MIN_SCORE = 0.0

Encode = Callable[[Sequence[str]], list[list[float]]]

# Shown to the model as "{sumber} · {judul_bab} · hlm. {halaman}". Fill in the full
# titles approved by DR for 54, 20, and 57.
SOURCE_TITLES = {
    "29": "Kemenkes RI · KMK HK.01.07/MENKES/1186/2022 (PPK Dokter di FKTP) · 2022",
    "54": "Dokumen 54 (Skistosomiasis)",
    "3": "AAFP · Acute diarrhea in adults, Am Fam Physician 106(1) · 2022",
    "6": "Deps et al. · WHO Skin NTDs app untuk deteksi kusta, Rev Panam Salud Publica · 2025",
    "4": "Barrera dkk. · Dengue, chikungunya, dan Zika di wilayah tropis (anak) · 2023",
    "10": "FEBRASGO · Protokol dengue pada kehamilan dan nifas, RBGO 46 · 2024",
    "20": "Kemenkes RI · Permenkes No. 8 Tahun 2017 (Eradikasi Frambusia) · 2017",
    "23": "Kemenkes RI · Permenkes No. 11 Tahun 2019 (Penanggulangan Kusta) · 2019",
    "42": "Mohiuddin · Penggunaan NSAID yang keliru pada COVID-19, dengue, chikungunya · 2023",
    "57": "Sharp dkk. · Karakteristik klinis chikungunya dan dengue, Clin Infect Dis 73(2) · 2021",
    "61": "NLM DailyMed · Monografi loperamid HCl kapsul · 2024",
    "67": "WHO · Dengue: pedoman diagnosis, tatalaksana, pencegahan, dan pengendalian · 2009",
    "69": "WHO · Ending the neglect (kerangka skin NTD terintegrasi) · 2022",
}


class Embedder:
    """Prefixes plus an encode function. Tests pass their own `encode`."""

    def __init__(self, encode: Encode) -> None:
        self._encode = encode

    def queries(self, texts: Sequence[str]) -> list[list[float]]:
        return self._check(self._encode([QUERY_PREFIX + t for t in texts]))

    def documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self._check(self._encode([DOC_PREFIX + t for t in texts]))

    @staticmethod
    def _check(vectors: list[list[float]]) -> list[list[float]]:
        for v in vectors:
            if len(v) != DIMS:
                raise ValueError(f"expected {DIMS} dimensions, got {len(v)}")
            if abs(math.sqrt(math.sumprod(v, v)) - 1.0) > 1e-3:
                raise ValueError("vectors must be L2 normalised")
        return vectors


def load_embedder(model_id: str = MODEL_ID) -> Embedder:
    """EmbeddingGemma 2 as the model card asks for text-only retrieval on a CPU."""
    st = importlib.import_module("sentence_transformers")
    torch = importlib.import_module("torch")
    model: Any = st.SentenceTransformer(
        model_id,
        device="cpu",
        model_kwargs={"torch_dtype": torch.float32},  # never float16: it gives NaN
        config_kwargs={"vision_config": None, "audio_config": None},  # text only
    )

    def encode(texts: Sequence[str]) -> list[list[float]]:
        out = model.encode(
            list(texts),
            batch_size=8,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return [[float(x) for x in row] for row in out]

    return Embedder(encode)


def split_untagged(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    tagged: list[dict[str, object]] = []
    untagged: list[dict[str, object]] = []
    for r in rows:
        (tagged if section_of(str(r["teks"])) else untagged).append(r)
    return tagged, untagged


def citation(r: dict[str, object]) -> str:
    title = SOURCE_TITLES.get(str(r["sumber"])) or f"Dokumen {r['sumber']}"
    page = f" · hlm. {r['halaman']}" if r["halaman"] else ""
    return f"{title} · {r['judul_bab']}{page}"


def build(
    flow_id: str,
    rows: list[dict[str, object]],
    embedder: Embedder,
    *,
    keep_untagged: bool = False,
) -> dict[str, object]:
    content = get_content(flow_id)
    scored = set(content.scored_diseases)
    rows = [r for r in rows if r["disease"] in scored]
    if not keep_untagged:
        rows, dropped = split_untagged(rows)
        if dropped:
            by_src: dict[str, int] = {}
            for r in dropped:
                by_src[str(r["sumber"])] = by_src.get(str(r["sumber"]), 0) + 1
            sys.stderr.write(
                f"warning: {len(dropped)} cards without a [Penyakit · Bagian] tag "
                f"skipped (per source: {by_src}); use --keep-untagged to keep them\n"
            )
    chunks = {
        f"c{i:03d}": {
            "disease": str(r["disease"]),
            "citation": citation(r),
            "text": " ".join(str(r["teks"]).split()),
        }
        for i, r in enumerate(rows, start=1)
    }
    ids = list(chunks)
    doc_vecs = embedder.documents([chunks[c]["text"] for c in ids])
    by_disease: dict[str, list[int]] = {}
    for i, cid in enumerate(ids):
        by_disease.setdefault(chunks[cid]["disease"], []).append(i)

    def ranked(qvec: list[float], disease: str) -> list[list[object]]:
        hits = [
            (ids[i], round(math.sumprod(qvec, doc_vecs[i]), 4))
            for i in by_disease.get(disease, [])
        ]
        hits = [(c, s) for c, s in hits if s > MIN_SCORE]
        hits.sort(key=lambda h: h[1], reverse=True)
        return [[c, s] for c, s in hits[:TOP_PER_DISEASE]]

    queries = option_queries(content)
    qvecs = dict(zip(queries, embedder.queries(list(queries.values())), strict=True))
    options: dict[str, dict[str, list[list[object]]]] = {}
    for key, qvec in qvecs.items():
        per = {d: h for d in sorted(by_disease) if (h := ranked(qvec, d))}
        if per:
            options[key] = per
    # No answer points anywhere: the disease's own name and the usual PPK headings.
    diseases = sorted(by_disease)
    dvecs = embedder.queries(
        [f"{content.diseases[d].name} hasil anamnesis gejala keluhan" for d in diseases]
    )
    default = {
        d: [str(c) for c, _ in ranked(v, d)]
        or [ids[i] for i in by_disease[d][:TOP_PER_DISEASE]]
        for d, v in zip(diseases, dvecs, strict=True)
    }
    missing = sorted(scored - set(by_disease))
    if missing:
        sys.stderr.write(f"warning: no chunks for {', '.join(missing)}\n")
    return {
        "version": FORMAT_VERSION,
        "flow_id": flow_id,
        "method": METHOD,
        "model": MODEL_ID,
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
    p.add_argument("--keep-untagged", action="store_true")
    args = p.parse_args()
    rows = [
        json.loads(line)
        for line in args.chunks.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    data = build(args.flow, rows, load_embedder(), keep_untagged=args.keep_untagged)
    out = args.out or DATA_DIR / f"{args.flow}_literature.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    n_chunks = len(data["chunks"])  # type: ignore[arg-type]
    n_keys = len(data["options"])  # type: ignore[arg-type]
    sys.stdout.write(f"{out}: {n_chunks} chunks, {n_keys} option keys\n")


if __name__ == "__main__":
    main()
