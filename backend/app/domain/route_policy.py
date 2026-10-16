"""Route decision and escalation: red flags, low score, cross-cutting vitals, severity signs.

The route decides where the patient is told to go, so the rules here follow the doctor's
answers (DR no. 15, Blueprint Tahap 7) and never the model.
"""

from app.domain.answers import Answers
from app.domain.warnings import missing_vitals
from app.triage.content import ROUTE_LEVEL, FlowContent, Option, RouteId
from app.triage.scoring import ScoreBreakdown, companion_shown, red_flag_ids, visible


def picked_options(answers: Answers, content: FlowContent) -> list[Option]:
    """Visible options the patient picked in the pattern and companion questions."""
    flow = content.flow
    c = answers.complaint or ""
    out: list[Option] = []
    pattern_q = flow.patterns.get(c)
    if pattern_q:
        out += [
            o
            for o in pattern_q.options
            if o.id == answers.pattern and visible(o, answers, content)
        ]
    companion_q = flow.companions.get(c)
    if companion_q and companion_shown(companion_q, answers):
        out += [o for o in companion_q.options if o.id in answers.companion]
    return out


def staff_notes_for(answers: Answers, content: FlowContent) -> list[str]:
    """Notes for the health worker from the picked options, without repeats."""
    if red_flag_ids(answers, content):
        return []
    notes = [o.staff_note for o in picked_options(answers, content) if o.staff_note]
    return list(dict.fromkeys(notes))


def decide_route(
    answers: Answers, content: FlowContent, b: ScoreBreakdown, flags: list[str]
) -> tuple[RouteId, bool, list[str]]:
    """(route, unknown, upgrade notes). `flags` are the patient's red flags."""
    w = content.weights
    top = b.ranked[0] if b.ranked else None
    no_thermo, no_bp = missing_vitals(answers, content)
    t = answers.temp if not no_thermo else None
    sys_bp = answers.bp_sys if not no_bp else None

    route: RouteId
    notes: list[str] = []
    if flags:
        # The browser already sent the patient to the red screen. Keep the server consistent.
        route, unknown = "red", False
    elif top is None or top.score < w.low_score_threshold:
        route, unknown = "yellow", True
    else:
        unknown = False
        route = content.diseases[top.id].route
        # Cross-cutting rules (DR no. 15, Blueprint Tahap 7): green becomes at least yellow.
        if route == "green":
            wn = content.advice.warnings
            if (
                w.high_fever_upgrade is not None
                and t is not None
                and t >= w.high_fever_upgrade
            ):
                route = "yellow"
                if wn.route_upgraded:
                    notes.append(wn.route_upgraded.format(temp=f"{t:.1f}"))
            if (
                w.bp_upgrade_above is not None
                and sys_bp is not None
                and sys_bp > w.bp_upgrade_above
            ):
                route = "yellow"
                if wn.route_upgraded_bp:
                    notes.append(wn.route_upgraded_bp.format(sys=sys_bp))
        # Severity signs (e.g. severe varicella, DR no. 8) raise the route too.
        for o in picked_options(answers, content):
            if o.min_route and ROUTE_LEVEL[o.min_route] > ROUTE_LEVEL[route]:
                route = o.min_route
                notes.append(
                    content.advice.warnings.route_upgraded_sign.format(
                        sign=(o.reason or o.text).lower()
                    )
                )
        # Weak top guess: green becomes yellow, and the patient is told to see a doctor.
        # Red, special and unknown are already at least yellow, so they keep their route.
        pct = round(top.share * 100)
        low_text = content.advice.warnings.low_confidence
        if w.refer_below_pct is not None and pct < w.refer_below_pct and route != "red":
            if route == "green":
                route = "yellow"
            if low_text:
                notes.append(low_text.format(pct=pct))
    return route, unknown, notes


def resolve_place(
    content: FlowContent, route: RouteId, unknown: bool, disease_id: str | None
) -> tuple[str, str]:
    """(place, maps_query) for the navigation button.

    A disease-specific place wins; otherwise the route default. An unknown guess always
    points at the plain yellow route, even when the red flags pushed the route to red.
    """
    route_info = content.flow.routes[route]
    if unknown:
        return route_info.place, content.flow.routes["yellow"].maps_query
    disease = content.diseases[disease_id] if disease_id else None
    place = (disease.place if disease and disease.place else None) or route_info.place
    maps_query = (
        disease.maps_query if disease and disease.maps_query else None
    ) or route_info.maps_query
    return place, maps_query
