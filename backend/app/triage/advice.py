"""Turn scores into what the patient sees: route, warnings, todo list, and summary.

Ported from the prototype's decide(), drugFlags(), crossVal(), adviceFor(), and
summary(). All patient-facing text comes from content/<flow>/advice.json (DR).

The pieces now live in app/domain -- route_policy (route + escalation), warnings
("Catatan penting" and the drug pop-ups), narration (the guessing steps) and summary (the
plain text + structured rows). This module stays the entry point and only wires them together.
"""

from app.domain.answers import Answers
from app.domain.narration import analysis_steps, cross_checks, meter, pct
from app.domain.route_policy import decide_route, resolve_place, staff_notes_for
from app.domain.summary import summary, summary_rows, summary_text
from app.domain.warnings import drug_flags as drug_flags  # re-exported for callers
from app.domain.warnings import red_flags, warnings_for
from app.triage.content import FlowContent
from app.triage.schemas import RankedDisease, ScoreResult
from app.triage.scoring import ScoreBreakdown, red_flag_ids

__all__ = [
    "build_result",
    "drug_flags",
    "red_flags",
    "summary",
    "summary_rows",
    "summary_text",
]


def build_result(
    flow_id: str,
    answers: Answers,
    content: FlowContent,
    b: ScoreBreakdown,
    drug_classes: frozenset[str] = frozenset(),
) -> ScoreResult:
    """`drug_classes`: classes the drug recognizer found in `answers.drugs` (may be empty)."""
    flow, advice = content.flow, content.advice
    flags = red_flag_ids(answers, content)
    ranked = b.ranked
    top = ranked[0] if ranked else None

    route, unknown, notes = decide_route(answers, content, b, flags)

    def public(r_id: str, score: float, share: float) -> RankedDisease:
        d = content.diseases[r_id]
        return RankedDisease(
            id=r_id, name=d.name, emoji=d.emoji, score=score, pct=pct(share)
        )

    top_public = (
        public(top.id, top.score, top.share)
        if top and not unknown and not flags
        else None
    )
    others_src = ranked[0:3] if unknown else ranked[1:4]
    others = [public(r.id, r.score, r.share) for r in others_src]

    disease = content.diseases[top.id] if top_public and top else None
    route_info = flow.routes[route]

    staff_notes = staff_notes_for(answers, content)
    warns, drug_popups = warnings_for(
        answers,
        content,
        b,
        route,
        unknown,
        flags,
        notes,
        staff_notes,
        drug_classes=drug_classes,
    )

    # "Yang perlu dilakukan".
    care = disease.care if disease else []
    todo: list[str]
    if route == "green":
        todo = [*advice.todo.green_before, *care]
    elif route == "yellow":
        todo = [
            *(care if disease else advice.todo.yellow_unknown),
            *advice.todo.yellow_after,
        ]
    elif route == "special":
        todo = [*advice.todo.special_before, *care]
    else:
        todo = []

    place, maps_query = resolve_place(
        content, route, unknown, top.id if top_public and top else None
    )

    checks = cross_checks(answers, content, b.scores)
    analysis = analysis_steps(answers, content, checks)
    candidates, meter_pct = meter(ranked, content, top)

    rows = summary_rows(answers, content, route, top_public, unknown)

    return ScoreResult(
        flow_id=flow_id,
        route=route,
        unknown=unknown,
        top=top_public,
        others=others,
        meter_candidates=candidates,
        meter_pct=meter_pct,
        reasons=b.reasons.get(top.id, [])[:6] if top_public and top else [],
        cross_checks=[text for _, text in checks] if top_public else [],
        warnings=warns,
        drug_popups=drug_popups,
        todo=todo,
        place=place,
        maps_query=maps_query,
        nav_label=route_info.nav_label,
        analysis_steps=analysis,
        summary=summary_text(rows),
        summary_rows=rows,
    )
