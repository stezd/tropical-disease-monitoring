"""build_literature.build() with a fake embedder: no model download, no torch."""

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

np = pytest.importorskip("numpy")

from app.triage.ai.literature import (  # noqa: E402
    Literature,
    get_literature,
    option_queries,
)
from app.triage.content import get_content  # noqa: E402

SCRIPT = Path(__file__).parents[3] / "scripts" / "build_literature.py"


@pytest.fixture(scope="module")
def builder() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_literature", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fake_embed(texts: list[str], _kind: str) -> np.ndarray:
    """Hashed bag of words in 768 dimensions, normalised. Same words, same direction."""
    out = np.zeros((len(texts), 768), dtype=np.float32)
    for row, text in zip(out, texts, strict=True):
        for w in text.lower().split():
            h = int(hashlib.md5(w.encode()).hexdigest(), 16)  # noqa: S324
            row[h % 768] += 1.0
    norms = np.linalg.norm(out, axis=1, keepdims=True)
    return out / np.maximum(norms, 1e-9)


ROWS = [
    {
        "disease": d,
        "sumber": "29",
        "judul_bab": "Bab",
        "halaman": h,
        "teks": f"[{d} · {sec}] {txt}",
    }
    for d, sec, txt, h in [
        ("malaria", "Gejala", "demam menggigil berulang berkeringat", 10),
        ("malaria", "Tatalaksana", "artemisinin primakuin", 11),
        ("dbd", "Gejala", "demam tinggi mendadak nyeri belakang mata", 20),
        ("dbd", "Kriteria Diagnosis", "demam bintik merah trombosit turun", ""),
        ("kusta", "Gejala", "bercak kulit mati rasa saraf menebal", 30),
        ("rabies", "Gejala", "takut air", 40),
    ]
]


def test_build_writes_the_format_the_runtime_reads(
    builder: ModuleType, tmp_path: Path
) -> None:
    data = builder.build("infection", ROWS, fake_embed)
    assert data["method"] == "embedding-v1"
    assert len(data["chunks"]) == 5  # rabies is not scored in the flow
    assert any(
        c["citation"].endswith("Bab") for c in data["chunks"].values()
    )  # no page
    path = tmp_path / "infection_literature.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    lit = Literature.load(path)  # validates every chunk id
    assert lit.version.startswith("embedding-v1@")
    assert set(lit.default) == {"malaria", "dbd", "kusta"}
    assert set(lit.options) <= set(option_queries(get_content("infection")))


def test_ranking_is_per_disease_and_by_similarity(builder: ModuleType) -> None:
    data = builder.build("infection", ROWS, fake_embed)
    hits = data["options"]["pattern:A:malaria"]["malaria"]
    top = data["chunks"][hits[0][0]]
    assert top["disease"] == "malaria"
    assert [s for _, s in hits] == sorted((s for _, s in hits), reverse=True)
    for per in data["options"].values():
        for disease, ranked in per.items():
            assert all(data["chunks"][c]["disease"] == disease for c, _ in ranked)


def test_min_score_drops_weak_hits(builder: ModuleType) -> None:
    data = builder.build("infection", ROWS, fake_embed, min_score=0.99)
    assert not any(
        s < 0.99 for per in data["options"].values() for r in per.values() for _, s in r
    )
    assert set(data["default"]) == {"malaria", "dbd", "kusta"}  # default never empty


def test_bad_vectors_are_refused(builder: ModuleType) -> None:
    def nan_embed(texts: list[str], _kind: str) -> np.ndarray:
        return np.full((len(texts), 768), np.nan, dtype=np.float32)

    with pytest.raises(ValueError, match="NaN"):
        builder.build("infection", ROWS, nan_embed)


def test_cache_is_not_poisoned_by_other_tests() -> None:
    get_literature.cache_clear()
