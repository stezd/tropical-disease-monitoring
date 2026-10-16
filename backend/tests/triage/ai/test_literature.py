import itertools

import pytest

from app.domain.answers import Answers
from app.triage.ai.config import DATA_DIR
from app.triage.ai.literature import (
    Literature,
    answer_keys,
    as_sources,
    get_literature,
    option_queries,
    retrieval_text,
)
from app.triage.content import FlowContent, get_content


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Mencret >3x sehari, tanpa darah", "Mencret >3x sehari"),
        ("Nyeri sendi berat, tanpa sakit kepala", "Nyeri sendi berat"),
        (
            "Lebih dari 3 bulan, kulit TIDAK mencekung saat ditekan jari, tetap bengkak",
            "Lebih dari 3 bulan, kulit , tetap bengkak",
        ),
        ("Imunisasi anak belum lengkap", "Imunisasi anak"),
        ("Batuk lebih dari 2 minggu", "Batuk lebih dari 2 minggu"),
    ],
)
def test_negative_clauses_cut_for_retrieval(text: str, expected: str) -> None:
    assert retrieval_text(text) == expected


def test_every_answer_key_is_a_known_option(content: FlowContent) -> None:
    known = set(option_queries(content))
    flow = content.flow
    for cluster in flow.clusters:
        pq = flow.patterns.get(cluster.id)
        patterns = [o.id for o in pq.options] if pq else [None]
        cq = flow.companions.get(cluster.id)
        companions = [[o.id] for o in cq.options] if cq else [[]]
        for p, comp in itertools.product(patterns, companions):
            a = Answers(
                age=8,
                complaint=cluster.id,
                pattern=p,
                companion=comp,
                eco=[o.id for o in flow.eco],
                body=[r.id for r in flow.body_regions],
                no_thermo=True,
                vital_proxy=[o.id for o in flow.vital_proxies["temp"]],
            )
            assert set(answer_keys(a, content)) <= known


def test_shipped_index_is_consistent(content: FlowContent) -> None:
    get_literature.cache_clear()
    lit = get_literature(DATA_DIR, "infection")
    assert lit.chunks, "run scripts/build_literature.py"
    diseases = {c.disease for c in lit.chunks.values()}
    assert diseases <= set(content.scored_diseases)
    assert set(lit.default) == diseases
    assert set(lit.options) <= set(option_queries(content))


def test_for_disease_only_returns_that_disease(content: FlowContent) -> None:
    lit = get_literature(DATA_DIR, "infection")
    keys = answer_keys(
        Answers(complaint="A", pattern="malaria", eco=["timur"]), content
    )
    for d in content.scored_diseases:
        chunks = lit.for_disease(d, keys, 3)
        assert all(c.disease == d for c in chunks)
    # No matching answer: the disease's default excerpts.
    assert lit.for_disease("kusta", [], 2)
    assert lit.for_disease("malaria", keys, 0) == []


def test_sources_are_labelled() -> None:
    lit = Literature(
        {
            "chunks": {
                "c1": {"disease": "dbd", "citation": "Buku · Bab · hlm. 1", "text": "x"}
            },
            "default": {"dbd": ["c1"]},
        }
    )
    [s] = as_sources(lit.for_disease("dbd", [], 1))
    assert (s.id, s.citation) == ("S1", "dbd · Buku · Bab · hlm. 1")


def test_missing_file_means_no_sources() -> None:
    lit = Literature.load(DATA_DIR / "does_not_exist.json")
    assert lit.for_disease("dbd", [], 3) == []


def _lit(chunks: dict[str, str], default: list[str], options: dict) -> Literature:
    return Literature(
        {
            "chunks": {
                cid: {"disease": "dbd", "citation": "x", "text": text}
                for cid, text in chunks.items()
            },
            "default": {"dbd": default},
            "options": options,
        }
    )


SECTIONS = {
    "t": "[Dengue · Tatalaksana] Beri cairan.",
    "g": "[Dengue · Gejala] Demam tinggi mendadak.",
    "k": "[Dengue · Kriteria Diagnosis] Demam 2 sampai 7 hari ditambah dua tanda.",
    "p": "[Dengue · Pencegahan] Berantas sarang nyamuk.",
    "n": "Teks tanpa awalan.",
}


def test_section_is_read_from_the_prefix() -> None:
    lit = _lit(SECTIONS, [], {})
    assert {c: lit.chunks[c].section for c in SECTIONS} == {
        "t": "Tatalaksana",
        "g": "Gejala",
        "k": "Kriteria Diagnosis",
        "p": "Pencegahan",
        "n": "",
    }
    assert lit.chunks["n"].weight == 1.0


def test_symptom_cards_beat_closer_treatment_cards() -> None:
    lit = _lit(
        SECTIONS,
        [],
        {"pattern:A:dbd": {"dbd": [["t", 0.62], ["g", 0.50], ["k", 0.48]]}},
    )
    got = [c.id for c in lit.for_disease("dbd", ["pattern:A:dbd"], 3)]
    assert got == ["g", "k", "t"]


def test_exposure_answers_have_no_section_preference() -> None:
    lit = _lit(
        SECTIONS,
        [],
        {"eco:banjir": {"dbd": [["p", 0.60], ["g", 0.55]]}},
    )
    assert [c.id for c in lit.for_disease("dbd", ["eco:banjir"], 2)] == ["p", "g"]


def test_default_excerpts_put_symptom_cards_first() -> None:
    lit = _lit(SECTIONS, ["t", "p", "k", "g"], {})
    assert [c.id for c in lit.for_disease("dbd", [], 2)] == ["k", "g"]


def test_section_weights_do_not_hide_cards_when_nothing_else_exists() -> None:
    lit = _lit({"t": SECTIONS["t"]}, ["t"], {})
    assert [c.id for c in lit.for_disease("dbd", [], 3)] == ["t"]
