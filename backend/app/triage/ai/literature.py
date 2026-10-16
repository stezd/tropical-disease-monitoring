"""Pre-computed literature lookup. No embedding model and no embedding call at runtime.

The form is multiple choice, so "which excerpts fit this answer" is computed once,
offline, for every option, and saved as data/<flow_id>_literature.json:

    {
      "version": 1, "flow_id": "infection", "method": "bm25-v1", "built_at": "...",
      "chunks":  {"c001": {"disease": "tbc", "citation": "...", "text": "..."}},
      "default": {"tbc": ["c003", "c001"]},            # when no answer points anywhere
      "options": {"pattern:tbc": {"tbc": [["c003", 4.1], ["c001", 2.0]]}}
    }

Cards start with a "[Penyakit · Bagian]" tag; for_disease() favours the Gejala and
Kriteria Diagnosis ones (see SYMPTOM_BOOST). Option keys come from `option_queries()` (offline) and `answer_keys()` (runtime), so both
sides always agree. Any builder (BM25 script, Colab with EmbeddingGemma) only has to
write this format. Excerpts are always looked up per disease: the model only sees
literature labelled with the candidate it is about.
"""

import json
import logging
import re
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any

from app.domain.answers import Answers
from app.triage.content import NONE_ID, FlowContent, Option
from app.triage.medgemma import Source
from app.triage.scoring import companion_shown, visible

logger = logging.getLogger("app.triage.ai")

FORMAT_VERSION = 1

# Every card text starts with "[Penyakit · Bagian] ...", the PPK heading it was cut from.
# The patient's answers are symptom facts, so cards about symptoms and diagnostic
# criteria are what the model should see first. Tatalaksana, Komplikasi, Pencegahan
# and the like are only useful when they match much better. Cards without a tag
# (no heading) get no boost.
SYMPTOM_SECTIONS = frozenset({"gejala", "kriteria diagnosis"})
# Multiplies the summed score of a Gejala / Kriteria Diagnosis card. Measured with
# EmbeddingGemma 2 (16 Oct 2026): cosine scores of the top cards sit within about
# 0.67 to 0.78 of each other, so 1.05 already means "a symptom card wins if it is
# within about 5% of the best card". 1.3 would act as a hard tier. Tune with the A/B test.
SYMPTOM_BOOST = 1.05
_SECTION = re.compile(r"^\[[^\]·]*·\s*([^\]]+?)\s*\]")


def section_of(text: str) -> str:
    """Heading from the `[Penyakit · Bagian]` tag at the start of a card, lower-cased."""
    m = _SECTION.match(text)
    return m.group(1).lower() if m else ""


# Negative clauses inside option texts ("tanpa darah", "TIDAK mencekung", "belum lengkap").
# A search for "tanpa darah" finds excerpts about blood, the opposite of the answer, so
# they are cut for retrieval only. The model always sees the full option text.
_NEGATIVE = re.compile(r"\b(tanpa|tidak|belum)\b[^,;()]*", re.IGNORECASE)


def retrieval_text(text: str) -> str:
    return re.sub(r"\s+", " ", _NEGATIVE.sub(" ", text)).strip(" ,;")


def _option_text(o: Option) -> str:
    return " ".join(t for t in (o.text, o.reason or "") if t)


def option_queries(content: FlowContent) -> dict[str, str]:
    """Every option key of the flow and the search text behind it (for builders)."""
    flow = content.flow
    q: dict[str, str] = {}
    for c in flow.clusters:
        q[f"cluster:{c.id}"] = f"{c.name} {c.sub}"
    for cid, pq in flow.patterns.items():
        for o in pq.options:
            if o.id != NONE_ID:
                q[f"pattern:{cid}:{o.id}"] = _option_text(o)
    for cid, cq in flow.companions.items():
        for o in cq.options:
            if o.id != NONE_ID:
                q[f"companion:{cid}:{o.id}"] = _option_text(o)
    for o in flow.eco:
        if o.id != NONE_ID:
            q[f"eco:{o.id}"] = _option_text(o)
    for vital, opts in flow.vital_proxies.items():
        for o in opts:
            if o.id != NONE_ID:
                q[f"vital:{vital}:{o.id}"] = _option_text(o)
    for r in flow.body_regions:
        q[f"body:{r.id}"] = f"nyeri {r.name}"
    return {k: retrieval_text(v) for k, v in q.items()}


def answer_keys(a: Answers, content: FlowContent) -> list[str]:
    """Option keys the patient picked, in quiz order."""
    flow = content.flow
    keys: list[str] = []
    cluster = next((c for c in flow.clusters if c.id == a.complaint), None)
    if cluster:
        keys.append(f"cluster:{cluster.id}")
        pq = flow.patterns.get(cluster.id)
        if pq and a.pattern and a.pattern != NONE_ID:
            opt = next((o for o in pq.options if o.id == a.pattern), None)
            if opt and visible(opt, a, content):
                keys.append(f"pattern:{cluster.id}:{opt.id}")
        cq = flow.companions.get(cluster.id)
        if cq and companion_shown(cq, a):
            keys += [
                f"companion:{cluster.id}:{o.id}"
                for o in cq.options
                if o.id != NONE_ID and o.id in a.companion
            ]
    keys += [
        f"eco:{o.id}"
        for o in flow.eco
        if o.id != NONE_ID and o.id in a.eco and visible(o, a, content)
    ]
    for vital, opts in flow.vital_proxies.items():
        keys += [
            f"vital:{vital}:{o.id}"
            for o in opts
            if o.id != NONE_ID and o.id in a.vital_proxy
        ]
    keys += [f"body:{r.id}" for r in flow.body_regions if r.id in a.body]
    return keys


@dataclass(frozen=True)
class Chunk:
    id: str
    disease: str
    citation: str
    text: str

    @property
    def section(self) -> str:
        return section_of(self.text)

    @property
    def is_symptom_card(self) -> bool:
        return self.section in SYMPTOM_SECTIONS


class Literature:
    """Excerpts for one flow. Empty when the file does not exist (no sources sent)."""

    def __init__(self, data: dict[str, Any] | None) -> None:
        data = data or {}
        self.version: str = f"{data.get('method', 'none')}@{data.get('built_at', '-')}"
        self.chunks: dict[str, Chunk] = {
            cid: Chunk(cid, c["disease"], c["citation"], c["text"])
            for cid, c in (data.get("chunks") or {}).items()
        }
        self.default: dict[str, list[str]] = data.get("default") or {}
        self.options: dict[str, dict[str, list[list[Any]]]] = data.get("options") or {}

    @classmethod
    def load(cls, path: Path) -> Literature:
        if not path.exists():
            logger.warning("no literature file at %s: model gets no sources", path)
            return cls(None)
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("version") != FORMAT_VERSION:
            raise ValueError(f"{path}: literature format {data.get('version')!r}")
        lit = cls(data)
        known = set(lit.chunks)
        refs = {c for ids in lit.default.values() for c in ids} | {
            c
            for per in lit.options.values()
            for ranked in per.values()
            for c, _ in ranked
        }
        if missing := refs - known:
            raise ValueError(f"{path}: unknown chunk ids {sorted(missing)[:5]}")
        return lit

    def for_disease(
        self,
        disease: str,
        keys: list[str],
        k: int,
        symptom_boost: float = SYMPTOM_BOOST,
    ) -> list[Chunk]:
        """Top `k` excerpts about `disease` for the picked options (summed scores).

        Gejala and Kriteria Diagnosis cards have their score multiplied by
        `symptom_boost` (1.0 = off), and come first among the default excerpts.
        """
        if k <= 0:
            return []
        total: dict[str, float] = {}
        for key in keys:
            for cid, score in self.options.get(key, {}).get(disease, []):
                total[cid] = total.get(cid, 0.0) + float(score)
        for cid in total:
            if self.chunks[cid].is_symptom_card:
                total[cid] *= symptom_boost
        ranked = sorted(total, key=lambda c: total[c], reverse=True)
        fallback = [c for c in self.default.get(disease, []) if c not in total]
        fallback.sort(key=lambda c: not self.chunks[c].is_symptom_card)  # stable
        return [self.chunks[c] for c in (ranked + fallback)[:k]]


def as_sources(chunks: list[Chunk]) -> list[Source]:
    """Numbered S1..Sn, each citation starting with the disease ID it is about."""
    return [
        Source(id=f"S{i}", citation=f"{c.disease} · {c.citation}", text=c.text)
        for i, c in enumerate(chunks, start=1)
    ]


@cache
def get_literature(directory: Path, flow_id: str) -> Literature:
    return Literature.load(directory / f"{flow_id}_literature.json")
