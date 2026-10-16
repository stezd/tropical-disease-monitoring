"""The offline builder (scripts/build_literature.py) with a fake encoder, and the
Gejala / Kriteria Diagnosis priority in Literature.for_disease. No model download."""

import hashlib
import importlib.util
import json
import math
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

import pytest

from app.domain.answers import Answers
from app.triage.ai.literature import (
    Literature,
    answer_keys,
    section_of,
)
from app.triage.content import FlowContent, get_content

SCRIPT = Path(__file__).parents[3] / "scripts" / "build_literature.py"
CORPUS = Path(__file__).parents[3] / "app/triage/ai/data/infection_chunks.jsonl"


def _load_script() -> ModuleType:
    spec = importlib.util.spec_from_file_location("build_literature", SCRIPT)
    assert spec
    assert spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bl = _load_script()


def fake_encode(texts: Sequence[str]) -> list[list[float]]:
    """Hashed bag of words, 768 dims, unit length. Shared words = higher cosine."""
    out = []
    for t in texts:
        v = [0.0] * bl.DIMS
        for w in t.lower().split():
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % bl.DIMS] += 1.0
        n = math.sqrt(sum(x * x for x in v)) or 1.0
        out.append([x / n for x in v])
    return out


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


@pytest.fixture(scope="module")
def built() -> dict[str, object]:
    rows = [json.loads(x) for x in CORPUS.read_text(encoding="utf-8").splitlines() if x]
    return bl.build("infection", rows, bl.Embedder(fake_encode))  # type: ignore[no-any-return]


def test_prefixes_are_the_ones_from_the_model_card() -> None:
    seen: list[str] = []

    def spy(texts: Sequence[str]) -> list[list[float]]:
        seen.extend(texts)
        return fake_encode(texts)

    e = bl.Embedder(spy)
    e.queries(["demam"])
    e.documents(["kartu"])
    assert seen == ["task: search result | query: demam", "title: none | text: kartu"]


def test_wrong_dimension_or_unnormalised_is_refused() -> None:
    with pytest.raises(ValueError, match="768"):
        bl.Embedder(lambda t: [[1.0] * 10 for _ in t]).queries(["x"])
    with pytest.raises(ValueError, match="normalised"):
        bl.Embedder(lambda t: [[1.0] * bl.DIMS for _ in t]).queries(["x"])


def test_built_file_matches_the_runtime_format(
    built: dict[str, object], content: FlowContent, tmp_path: Path
) -> None:
    assert built["method"] == "embedding-v1"
    path = tmp_path / "infection_literature.json"
    path.write_text(json.dumps(built, ensure_ascii=False), encoding="utf-8")
    lit = Literature.load(path)  # raises on a bad version or unknown chunk ids
    assert lit.version.startswith("embedding-v1@")
    diseases = {c.disease for c in lit.chunks.values()}
    assert diseases <= set(content.scored_diseases)
    assert set(lit.default) == diseases
    assert set(lit.options) <= set(bl.option_queries(content))
    assert len(lit.options) == 65


def test_every_card_is_tagged_and_scores_are_sorted(built: dict[str, object]) -> None:
    chunks: dict[str, dict[str, str]] = built["chunks"]  # type: ignore[assignment]
    assert all(section_of(c["text"]) for c in chunks.values())
    options: dict[str, dict[str, list[list[float]]]] = built["options"]  # type: ignore[assignment]
    for per in options.values():
        for disease, ranked in per.items():
            assert len(ranked) <= bl.TOP_PER_DISEASE
            assert [s for _, s in ranked] == sorted(
                (s for _, s in ranked), reverse=True
            )
            assert all(chunks[c]["disease"] == disease for c, _ in ranked)


def test_citation_skips_empty_page() -> None:
    row = {"sumber": "6", "judul_bab": "Pendahuluan", "halaman": None}
    assert not bl.citation(row).endswith("hlm. None")
    assert "hlm." not in bl.citation(row)
    assert bl.citation({**row, "halaman": 15}).endswith("Pendahuluan · hlm. 15")


def test_section_of() -> None:
    assert (
        section_of("[Malaria · Kriteria Diagnosis] Demam ...") == "kriteria diagnosis"
    )
    assert section_of("on. To manage this transition") == ""


def _lit() -> Literature:
    def chunk(disease: str, section: str) -> dict[str, str]:
        return {"disease": disease, "citation": "x", "text": f"[D · {section}] isi"}

    return Literature(
        {
            "chunks": {
                "c1": chunk("dbd", "Tatalaksana"),
                "c2": chunk("dbd", "Gejala"),
                "c3": chunk("dbd", "Komplikasi"),
                "c4": chunk("dbd", "Kriteria Diagnosis"),
            },
            "default": {"dbd": ["c1", "c3", "c4", "c2"]},
            "options": {
                "pattern:A:dbd": {"dbd": [["c1", 0.70], ["c2", 0.68], ["c3", 0.66]]}
            },
        }
    )


def test_symptom_cards_beat_slightly_closer_other_cards() -> None:
    lit = _lit()
    got = [c.id for c in lit.for_disease("dbd", ["pattern:A:dbd"], 3)]
    assert got[:2] == ["c2", "c1"]  # 0.68 * 1.05 = 0.714 > 0.70
    off = [
        c.id for c in lit.for_disease("dbd", ["pattern:A:dbd"], 3, symptom_boost=1.0)
    ]
    assert off[:2] == ["c1", "c2"]


def test_a_much_closer_non_symptom_card_still_wins() -> None:
    lit = _lit()
    lit.options["pattern:A:dbd"]["dbd"][0][1] = 0.80
    assert lit.for_disease("dbd", ["pattern:A:dbd"], 1)[0].id == "c1"


def test_default_cards_put_symptom_sections_first() -> None:
    got = [c.id for c in _lit().for_disease("dbd", [], 4)]
    assert got == ["c4", "c2", "c1", "c3"]


def test_boost_does_not_leak_across_diseases(content: FlowContent) -> None:
    lit = _lit()
    keys = answer_keys(Answers(complaint="A", pattern="dbd"), content)
    assert lit.for_disease("malaria", keys, 3) == []
