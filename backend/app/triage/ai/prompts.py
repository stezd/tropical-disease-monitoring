"""Prompts, message layout, and output schemas for both scoring modes.

The patient's drug text is never sent here: drugs have their own step (/drugs), so a
painkiller cannot pull a score down. Literature is always labelled with a disease ID.
"""

from typing import Any

from app.domain.answers import Answers
from app.triage.content import NONE_ID, FlowContent, Option
from app.triage.medgemma import FLOW_LABEL, Fact, Source, TextRequest
from app.triage.scoring import companion_shown, visible

# Bump when a prompt, the facts, the message layout, or a schema changes. Goes to the
# call log. ai-3: both branches had bumped to ai-2 separately (3-5 candidates with
# minItems; Gemma4 facts p2 without photo findings, GDS, blood pressure category,
# uric acid, cholesterol), merged here.
PROMPT_VERSION = "ai-3"

_SCALE = "0 = no match, 30 = weak, 50 = plausible, 70 = strong, 90 = textbook match"

SYSTEM_SINGLE = f"""\
You are a screening assistant for an Indonesian community health app. You do not diagnose.
Score how well each candidate disease matches the patient's facts, 0-100 ({_SCALE}).
Rules:
- Use only the patient facts. A sign that is not in the facts is absent; never assume it.
- The patient answered multiple-choice questions. "Ditanyakan, tidak dipilih" lists options
  they saw and did not pick: treat those signs as absent.
- Literature describes diseases, not this patient. Each excerpt starts with the disease ID
  it is about. Use it to judge how typical the facts are for that disease.
- Similar diseases must be separated by the facts that differ between them.
- evidence: fact IDs that support the score. sources: literature IDs you relied on.
- Use only the listed candidate, fact, and source IDs.
- Return the 3 to 5 best-matching candidates, highest score first. Always include the
  closest alternatives too, even when their scores are low (e.g. 10-30): staff need to
  see what else to rule out.
- note: one short sentence in Indonesian on why, for the review team.
Reply with JSON only."""

SYSTEM_ONE = f"""\
You are a screening assistant for an Indonesian community health app. You do not diagnose.
Score how well ONE candidate disease matches the patient's facts, 0-100 ({_SCALE}).
Rules:
- Use only the patient facts. A sign that is not in the facts is absent; never assume it.
- "Ditanyakan, tidak dipilih" lists signs of this candidate that the patient saw as options
  and did not pick. Treat them as absent and weigh them against the candidate.
- Literature describes the candidate, not this patient. Use it to judge how typical the
  facts are.
- A general fact (fever, a body area) that fits many diseases is weak support on its own.
- evidence: fact IDs that support this candidate. sources: literature IDs you relied on.
  Use only the listed IDs.
- note: one short sentence in Indonesian on why, for the review team.
Reply with JSON only."""


# ── "Asked, not picked" ────────────────────────────────────────────────────


def asked_not_picked(
    a: Answers, content: FlowContent, disease: str | None = None
) -> list[str]:
    """Options the patient saw and did not pick, as "label: text" lines.

    The form has no "no" options, so this is the only way the model learns that a sign
    was asked about and is absent. Only questions the patient answered count. With
    `disease`, only options that point to that disease, plus its cluster when the
    patient chose another one.
    """
    flow, w = content.flow, content.weights
    out: list[str] = []

    def add(label: str, text: str) -> None:
        line = f"{label}: {text}"
        if line not in out:
            out.append(line)

    def scan(
        label: str,
        options: list[Option],
        picked: list[str],
        targets_of: Any = None,
    ) -> None:
        for o in options:
            if o.id == NONE_ID or o.id in picked or not visible(o, a, content):
                continue
            targets = targets_of(o) if targets_of else o.targets()
            if disease is None or disease in targets:
                add(label, o.text)

    cluster = next((c for c in flow.clusters if c.id == a.complaint), None)
    if disease is not None and a.complaint is not None:
        for c in flow.clusters:
            if c.id != a.complaint and disease in c.members:
                add("Keluhan utama", c.name)
    if cluster:
        pq = flow.patterns.get(cluster.id)
        if pq and a.pattern:
            scan("Pola gejala", pq.options, [a.pattern], lambda o: o.targets(o.id))
        cq = flow.companions.get(cluster.id)
        if cq and companion_shown(cq, a) and a.companion:
            scan("Gejala penyerta", cq.options, a.companion)
    if a.eco:
        scan(
            "Riwayat / faktor risiko",
            flow.eco,
            a.eco,
            lambda o: list(w.eco.get(o.id, {})),
        )
    if disease is not None and a.body and w.body:
        names = {r.id: r.name for r in flow.body_regions}
        picked = set(a.body)
        rules = [(r.any, r.points) for r in w.body.rules]
        rules.append((w.body.joints.regions, {w.body.joints.disease: 1.0}))
        for regions, points in rules:
            if disease in points and not picked & set(regions):
                add("Nyeri", ", ".join(names.get(r, r) for r in regions))
    return out


# ── Messages ───────────────────────────────────────────────────────────────


def _facts(facts: list[Fact]) -> list[str]:
    return ["Fakta pasien:"] + [f"{f.id} {f.label}: {f.text}" for f in facts]


def _absent(lines: list[str]) -> list[str]:
    return (
        ["", "Ditanyakan, tidak dipilih:"] + [f"- {x}" for x in lines] if lines else []
    )


def _literature(sources: list[Source]) -> list[str]:
    if not sources:
        return []
    out = ["", "Literatur:"]
    for s in sources:
        out += [f"[{s.id}] {s.citation}", s.text, ""]
    return out


def single_message(req: TextRequest, absent: list[str]) -> str:
    lines = [f"Jalur: {FLOW_LABEL[req.flow_id]}", ""]
    lines += _facts(req.facts)
    lines += _absent(absent)
    lines += ["", "Kandidat:"] + [f"- {c.id}: {c.name}" for c in req.candidates]
    lines += _literature(req.sources)
    return "\n".join(lines).rstrip() + "\n"


def one_message(
    flow_id: str,
    candidate_id: str,
    candidate_name: str,
    facts: list[Fact],
    absent: list[str],
    sources: list[Source],
) -> str:
    lines = [
        f"Jalur: {FLOW_LABEL[flow_id]}",
        f"Kandidat: {candidate_id} ({candidate_name})",
        "",
    ]
    lines += _facts(facts)
    lines += _absent(absent)
    lines += _literature(sources)
    return "\n".join(lines).rstrip() + "\n"


# ── Output schemas (JSON Schema subset that Gemini and vLLM both accept) ──


def _ids(ids: list[str]) -> dict[str, Any]:
    if not ids:
        return {"type": "array", "items": {"type": "string"}, "maxItems": 0}
    return {"type": "array", "items": {"type": "string", "enum": ids}}


def _scored(
    fact_ids: list[str], source_ids: list[str], candidate_ids: list[str] | None
) -> dict[str, Any]:
    props: dict[str, Any] = {}
    if candidate_ids is not None:
        props["id"] = {"type": "string", "enum": candidate_ids}
    props["note"] = {"type": "string"}
    props["score"] = {"type": "integer", "minimum": 0, "maximum": 100}
    props["evidence"] = _ids(fact_ids)
    props["sources"] = _ids(source_ids)
    return {
        "type": "object",
        "properties": props,
        "required": list(props),
        "additionalProperties": False,
    }


def single_schema(req: TextRequest, max_candidates: int) -> dict[str, Any]:
    item = _scored(
        [f.id for f in req.facts],
        [s.id for s in req.sources],
        [c.id for c in req.candidates],
    )
    return {
        "type": "object",
        "properties": {
            "candidates": {
                "type": "array",
                # At least 3 so the result page has alternatives (fewer if the flow
                # has fewer candidates).
                "minItems": min(3, len(req.candidates), max_candidates),
                "maxItems": max_candidates,
                "items": item,
            }
        },
        "required": ["candidates"],
        "additionalProperties": False,
    }


def one_schema(facts: list[Fact], sources: list[Source]) -> dict[str, Any]:
    return _scored([f.id for f in facts], [s.id for s in sources], None)
