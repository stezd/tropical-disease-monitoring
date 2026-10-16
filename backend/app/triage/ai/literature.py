"""Pre-computed literature lookup. No embedding model and no embedding call at runtime.

The form is multiple choice, so "which excerpts fit this answer" is computed once,
offline, for every option, and saved as data/<flow_id>_literature.json:

    {
      "version": 1, "flow_id": "infection", "method": "embedding-v1", "built_at": "...",
      "chunks":  {"c001": {"disease": "tbc", "citation": "...", "text": "..."}},
      "default": {"tbc": ["c003", "c001"]},            # when no answer points anywhere
      "options": {"pattern:tbc": {"tbc": [["c003", 4.1], ["c001", 2.0]]}}
    }

Option keys come from `option_queries()` (offline) and `answer_keys()` (runtime), so both
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

# Negative clauses inside option texts ("tanpa darah", "TIDAK mencekung", "belum lengkap").
# A search for "tanpa darah" finds excerpts about blood, the opposite of the answer, so
# they are cut for retrieval only. The model always sees the full option text.
_NEGATIVE = re.compile(r"\b(tanpa|tidak|belum)\b[^,;()]*", re.IGNORECASE)


# Each excerpt starts with "[Penyakit · Bagian]". Facts the patient gave are symptoms, so
# the cards that describe symptoms and the diagnostic criteria come first; treatment,
# prevention and referral cards only fill the remaining slots. Weights multiply the
# retrieval score at runtime, so the JSON on disk does not change when they are tuned.
_SECTION = re.compile(r"^\[[^\]\n]*? · ([^\]\n]+)\]")
SECTION_WEIGHT: dict[str, float] = {
    "Gejala": 1.5,
    "Kriteria Diagnosis": 1.5,
    "Tatalaksana": 0.6,
    "Pencegahan": 0.6,
    "Kriteria Rujukan": 0.6,
}
# Exposure answers (flood, lake, crowded housing) are about where the disease comes
# from, which lives in Definisi and Pencegahan cards: no section preference there.
_UNWEIGHTED_KEYS = ("eco:",)


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
        """The card type from the "[Penyakit · Bagian]" prefix, "" when there is none."""
        m = _SECTION.match(self.text)
        return m.group(1).strip() if m else ""

    @property
    def weight(self) -> float:
        return SECTION_WEIGHT.get(self.section, 1.0)


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

    def for_disease(self, disease: str, keys: list[str], k: int) -> list[Chunk]:
        """Top `k` excerpts about `disease` for the picked options.

        Score = sum over picked options of retrieval score x section weight, so Gejala
        and Kriteria Diagnosis cards win over closer-matching Tatalaksana cards.
        """
        if k <= 0:
            return []
        total: dict[str, float] = {}
        for key in keys:
            plain = key.startswith(_UNWEIGHTED_KEYS)
            for cid, score in self.options.get(key, {}).get(disease, []):
                w = 1.0 if plain else self.chunks[cid].weight
                total[cid] = total.get(cid, 0.0) + float(score) * w
        ranked = sorted(total, key=lambda c: total[c], reverse=True)
        # sorted() is stable: inside a weight class the builder's order is kept.
        rest = [c for c in self.default.get(disease, []) if c not in total]
        rest.sort(key=lambda c: self.chunks[c].weight, reverse=True)
        return [self.chunks[c] for c in (ranked + rest)[:k]]


def as_sources(chunks: list[Chunk]) -> list[Source]:
    """Numbered S1..Sn, each citation starting with the disease ID it is about."""
    return [
        Source(id=f"S{i}", citation=f"{c.disease} · {c.citation}", text=c.text)
        for i, c in enumerate(chunks, start=1)
    ]


@cache
def get_literature(directory: Path, flow_id: str) -> Literature:
    return Literature.load(directory / f"{flow_id}_literature.json")
