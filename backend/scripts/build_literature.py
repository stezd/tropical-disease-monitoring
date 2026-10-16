"""Build app/triage/ai/data/<flow>_literature.json from a chunk file. Run offline, once.

    uv run --with sentence-transformers python scripts/build_literature.py \
        --flow infection --chunks app/triage/ai/data/infection_chunks.jsonl

Input: JSON lines with `disease`, `sumber`, `judul_bab`, `halaman`, `teks`
(the output of pemotong_dokumen.ipynb). Diseases not scored in the flow (rabies) are
skipped.

Ranking: every chunk and every option query is embedded with google/embeddinggemma-2
(text only, float32, CPU, 768 dimensions, L2-normalised). Score = cosine similarity.
Hits are kept per disease, so the model only ever gets excerpts about the candidate it
is scoring. The runtime does not load the model: it only reads the JSON this script
writes (see app/triage/ai/literature.py).

float16 must not be used with this model (activations overflow to NaN), and the model
is loaded without its vision and audio encoders (270M instead of 740M parameters).
"""

import argparse
import json
import sys
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from app.triage.ai.config import DATA_DIR
from app.triage.ai.literature import FORMAT_VERSION, option_queries
from app.triage.content import get_content

MODEL_ID = "google/embeddinggemma-2"
METHOD = "embedding-v1"
QUERY_PREFIX = "task: search result | query: "
DOC_PREFIX = "title: none | text: "
DIM = 768

# Shown to the model as "{sumber} · {judul_bab} · hlm. {halaman}". Keys are the
# bibliography numbers of the 75 documents.
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

TOP_PER_DISEASE = 5

# embed(texts, kind) -> (n, dim) float32, rows L2-normalised. kind is "query" or "doc".
Embedder = Callable[[list[str], str], np.ndarray]


def load_embedder() -> Embedder:
    """The real model. Imported here so tests and the runtime never need torch."""
    import torch
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(
        MODEL_ID,
        device="cpu",
        model_kwargs={"torch_dtype": torch.float32},
        config_kwargs={"vision_config": None, "audio_config": None},
    )

    def embed(texts: list[str], kind: str) -> np.ndarray:
        prefix = QUERY_PREFIX if kind == "query" else DOC_PREFIX
        out = model.encode(
            [prefix + t for t in texts],
            batch_size=16,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return np.asarray(out, dtype=np.float32)

    return embed


def _checked(vectors: np.ndarray, n: int, what: str) -> np.ndarray:
    if vectors.shape != (n, DIM):
        raise ValueError(f"{what}: shape {vectors.shape}, expected {(n, DIM)}")
    if not np.isfinite(vectors).all():
        raise ValueError(f"{what}: NaN or inf (float16 by accident?)")
    norms = np.linalg.norm(vectors, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-3):
        raise ValueError(f"{what}: vectors are not normalised")
    return vectors


def build(
    flow_id: str,
    rows: list[dict[str, object]],
    embed: Embedder,
    min_score: float = 0.0,
) -> dict[str, object]:
    content = get_content(flow_id)
    scored = set(content.scored_diseases)
    rows = [r for r in rows if r["disease"] in scored]
    chunks = {
        f"c{i:03d}": {
            "disease": str(r["disease"]),
            "citation": f"{SOURCE_TITLES.get(str(r['sumber']), f'Dokumen {r["sumber"]}')}"
            f" · {r['judul_bab']}" + (f" · hlm. {r['halaman']}" if r["halaman"] else ""),
            "text": " ".join(str(r["teks"]).split()),
        }
        for i, r in enumerate(rows, start=1)
    }
    ids = list(chunks)
    by_disease: dict[str, list[int]] = {}
    for i, cid in enumerate(ids):
        by_disease.setdefault(chunks[cid]["disease"], []).append(i)

    docs = embed([c["text"] for c in chunks.values()], "doc")
    queries = option_queries(content)
    qkeys = list(queries)
    qvecs = embed([queries[k] for k in qkeys], "query")
    defaults = {
        d: f"{content.diseases[d].name} hasil anamnesis gejala keluhan"
        for d in sorted(by_disease)
    }
    dvecs = embed(list(defaults.values()), "query")
    docs = _checked(docs, len(ids), "chunks")
    qvecs = _checked(qvecs, len(qkeys), "option queries")
    dvecs = _checked(dvecs, len(defaults), "default queries")

    def ranked(vec: np.ndarray, disease: str) -> list[tuple[str, float]]:
        idx = by_disease.get(disease, [])
        sims = docs[idx] @ vec
        hits = [(ids[i], round(float(s), 4)) for i, s in zip(idx, sims, strict=True)]
        hits = [h for h in hits if h[1] >= min_score]
        hits.sort(key=lambda h: h[1], reverse=True)
        return hits[:TOP_PER_DISEASE]

    options: dict[str, dict[str, list[list[object]]]] = {}
    seen: list[float] = []
    for key, vec in zip(qkeys, qvecs, strict=True):
        per = {d: [[c, s] for c, s in r] for d in sorted(by_disease) if (r := ranked(vec, d))}
        seen += [s for hits in per.values() for _, s in hits]
        if per:
            options[key] = per
    # No answer points anywhere: the disease's own name and the usual PPK headings.
    default = {
        d: [c for c, _ in ranked(v, d)] or [ids[i] for i in by_disease[d][:TOP_PER_DISEASE]]
        for d, v in zip(sorted(by_disease), dvecs, strict=True)
    }
    missing = sorted(scored - set(by_disease))
    if missing:
        sys.stderr.write(f"warning: no chunks for {', '.join(missing)}\n")
    if seen:
        p = np.percentile(seen, [5, 25, 50, 75, 95])
        sys.stderr.write(
            "kept-hit cosine p5/p25/p50/p75/p95: " + " ".join(f"{x:.3f}" for x in p) + "\n"
        )
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
    p.add_argument(
        "--min-score",
        type=float,
        default=0.0,
        help="drop hits below this cosine. Pick it from the percentiles printed "
        "by a first run (0 keeps the top 5 of every disease).",
    )
    args = p.parse_args()
    rows = [
        json.loads(line)
        for line in args.chunks.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    data = build(args.flow, rows, load_embedder(), args.min_score)
    out = args.out or DATA_DIR / f"{args.flow}_literature.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    n_chunks = len(data["chunks"])  # type: ignore[arg-type]
    n_keys = len(data["options"])  # type: ignore[arg-type]
    sys.stdout.write(f"{out}: {n_chunks} chunks, {n_keys} option keys\n")


if __name__ == "__main__":
    main()
