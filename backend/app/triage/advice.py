"""Turn scores into what the patient sees: route, warnings, todo list, and summary.

Ported from the prototype's decide(), drugFlags(), crossVal(), adviceFor(), and
summary(). All patient-facing text comes from content/<flow>/advice.json (DR).
"""

from app.triage.content import (
    NONE_ID,
    ROUTE_LEVEL,
    FlowContent,
    Option,
    RouteId,
)
from app.triage.schemas import Answers, RankedDisease, ScoreResult, Warning
from app.triage.scoring import (
    ScoreBreakdown,
    bmi,
    companion_shown,
    nutrition,
    visible,
)

JOINT_REGIONS = {"wrist_r", "wrist_l", "ankle_r", "ankle_l"}


def drug_flags(answers: Answers, content: FlowContent) -> list[str]:
    """Names of the advice.json drug rules that fire, in file order."""
    text = answers.drugs.lower()
    out: list[str] = []
    for name, rule in content.advice.drugs.items():
        if not any(k.lower() in text for k in rule.keywords):
            continue
        if rule.patterns and answers.pattern not in rule.patterns:
            continue
        if rule.complaints and answers.complaint not in rule.complaints:
            continue
        out.append(name)
    return out


def red_flags(answers: Answers) -> list[str]:
    return [f for f in answers.red_flags if f != NONE_ID]


def _fmt(n: float) -> str:
    return f"{n:g}"


def _pct(share: float) -> int:
    return round(share * 100)


def _no_thermo_text(answers: Answers, fever_pattern: str, other: str) -> str:
    return fever_pattern if answers.complaint == "A" else other


def _missing_vitals(answers: Answers, content: FlowContent) -> tuple[bool, bool]:
    """(no thermometer, no blood pressure meter), only for vitals this flow asks."""
    vitals = content.flow.vitals
    return (
        "temp" in vitals and answers.no_thermo,
        "bp" in vitals and answers.no_bp,
    )


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


def cross_checks(
    answers: Answers, content: FlowContent, s: dict[str, float]
) -> list[tuple[str, str]]:
    """(title, text) for each pair of look-alike diseases worth comparing."""
    out: list[tuple[str, str]] = []
    for check in content.advice.cross_checks:
        a, b = s.get(check.first_id, 0), s.get(check.second_id, 0)
        if answers.complaint in check.complaints or (a > 0 and b > 0):
            out.append(
                (
                    check.title,
                    check.text.format(winner=check.first if a > b else check.second),
                )
            )
    return out


def build_result(
    flow_id: str, answers: Answers, content: FlowContent, b: ScoreBreakdown
) -> ScoreResult:
    flow, advice, w = content.flow, content.advice, content.weights
    flags = red_flags(answers)
    ranked = b.ranked
    top = ranked[0] if ranked else None
    no_thermo, no_bp = _missing_vitals(answers, content)
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
            wn = advice.warnings
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
                    advice.warnings.route_upgraded_sign.format(
                        sign=(o.reason or o.text).lower()
                    )
                )

    def public(r_id: str, score: float, share: float) -> RankedDisease:
        d = content.diseases[r_id]
        return RankedDisease(
            id=r_id, name=d.name, emoji=d.emoji, score=score, pct=_pct(share)
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

    # Warnings ("Catatan penting").
    fired = drug_flags(answers, content)
    nut = nutrition(answers, content)
    body = set(answers.body)
    wn = advice.warnings
    warns: list[Warning] = []
    for name in fired:
        rule = advice.drugs[name]
        warns.append(Warning(level=rule.level, icon=rule.icon, text=rule.result))
    chik = w.chik_chronic_warning
    if (
        chik
        and wn.chik_chronic
        and body & JOINT_REGIONS
        and answers.pain is not None
        and answers.pain >= chik.pain_from
        and b.scores.get("chik", 0) >= chik.min_score
    ):
        warns.append(Warning(level="y", icon="🦴", text=wn.chik_chronic))
    if (
        wn.malaria_obese
        and w.malaria_obese_warning_min_score is not None
        and nut == "obes"
        and b.scores.get("malaria", 0) >= w.malaria_obese_warning_min_score
    ):
        warns.append(Warning(level="r", icon="⚠️", text=wn.malaria_obese))
    if (
        wn.high_fever
        and w.high_fever_upgrade is not None
        and t is not None
        and t >= w.high_fever_upgrade
    ):
        warns.append(
            Warning(level="r", icon="🌡️", text=wn.high_fever.format(temp=f"{t:.1f}"))
        )
    if not unknown and not flags:
        warns.extend(
            Warning(level=n.level, icon=n.icon, text=n.text)
            for n in advice.route_notes.get(route, [])
        )
    warns.extend(Warning(level="b", icon="⬆️", text=n) for n in notes)
    if no_thermo and wn.no_thermo_fever_pattern and wn.no_thermo_other:
        warns.append(
            Warning(
                level="b",
                icon="🌡️",
                text=_no_thermo_text(
                    answers, wn.no_thermo_fever_pattern, wn.no_thermo_other
                ),
            )
        )
    if no_bp and wn.no_bp:
        warns.append(Warning(level="b", icon="🩺", text=wn.no_bp))
    if bmi(answers) is None:
        warns.append(Warning(level="b", icon="🤖", text=wn.no_bmi))

    drug_popups = [
        Warning(level=advice.drugs[n].level, icon="⚠️", text=advice.drugs[n].popup)
        for n in fired
    ]

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

    if unknown:
        place, maps_query = route_info.place, flow.routes["yellow"].maps_query
    else:
        place = (
            disease.place if disease and disease.place else None
        ) or route_info.place
        maps_query = (
            disease.maps_query if disease and disease.maps_query else None
        ) or route_info.maps_query

    # Steps on the "Kak Tropi sedang menebak" screen.
    steps = advice.analysis_steps
    analysis = [steps.read]
    if no_thermo and steps.no_thermo_fever_pattern and steps.no_thermo_other:
        analysis.append(
            _no_thermo_text(
                answers, steps.no_thermo_fever_pattern, steps.no_thermo_other
            )
        )
    if no_bp and steps.no_bp:
        analysis.append(steps.no_bp)
    if bmi(answers) is None:
        analysis.append(steps.no_bmi)
    if not no_thermo and not no_bp and bmi(answers) is not None:
        analysis.append(steps.vitals_complete)
    checks = cross_checks(answers, content, b.scores)
    analysis.extend(steps.cross_check.format(title=title) for title, _ in checks)
    analysis.append(
        steps.eco.format(count=len([e for e in answers.eco if e != NONE_ID]))
    )
    if [f for f in answers.findings if f != NONE_ID]:
        analysis.append(steps.findings)
    analysis.append(steps.score)
    analysis.append(steps.route)

    candidates = max(1, len([r for r in ranked if r.share >= w.candidate_min_share]))
    meter_pct = min(w.max_display_pct, _pct(top.share)) if top else 0

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
        summary=summary(answers, content, route, top_public, unknown),
    )


def summary(
    answers: Answers,
    content: FlowContent,
    route: RouteId,
    top: RankedDisease | None,
    unknown: bool,
) -> str:
    """Plain-text summary for the copy button and the QR page. No name, NIK, or photo."""
    flow = content.flow
    a = answers

    def label(options: list[Option], oid: str | None) -> str | None:
        return next((o.text for o in options if o.id == oid), None)

    cluster = next((c for c in flow.clusters if c.id == a.complaint), None)
    if cluster:
        complaint = cluster.name
    elif a.complaint == NONE_ID:
        complaint = "tidak ada keluhan (cek risiko)"
    else:
        complaint = "-"
    pattern_q = flow.patterns.get(a.complaint or "")
    pattern = label(pattern_q.options, a.pattern) if pattern_q else None
    companion_q = flow.companions.get(a.complaint or "")
    companions = (
        [o.text for o in companion_q.options if o.id in a.companion and o.id != NONE_ID]
        if companion_q and companion_shown(companion_q, a)
        else []
    )
    eco = [o.reason or o.text for o in flow.eco if o.id in a.eco and o.id != NONE_ID]
    flags = [f for f in flow.red_flags if f.id in a.red_flags]
    b = bmi(a)
    no_thermo, no_bp = _missing_vitals(a, content)
    proxies = [
        o.text
        for opts in flow.vital_proxies.values()
        for o in opts
        if o.id in a.vital_proxy and o.id != NONE_ID
    ]
    if b is not None and a.height_cm is not None and a.weight_kg is not None:
        gizi = f"IMT {b:.1f} (TB {_fmt(a.height_cm)} cm, BB {_fmt(a.weight_kg)} kg)"
    else:
        gizi = "proksi: " + (label(flow.nutrition_proxies, a.nutrition_proxy) or "-")
    body = [r.name for r in flow.body_regions if r.id in a.body]
    pain = f" (nyeri {a.pain}/10)" if body and a.pain is not None else ""
    findings = [o.text for o in flow.findings if o.id in a.findings and o.id != NONE_ID]
    disease = content.diseases[top.id] if top else None
    r = flow.routes[route]
    when = a.taken_at.strftime("%d/%m/%Y %H.%M") if a.taken_at else "-"

    if unknown:
        dugaan = "belum dapat ditentukan"
    elif top and disease:
        dugaan = f"{disease.name} ({top.pct}%)"
    else:
        dugaan = "-"

    patient = [
        label(flow.who, a.who) or "-",
        f"{a.age} th" if a.age is not None else "-",
        label(flow.sex, a.sex) or "-",
    ]
    if a.pregnant is not None:
        patient.append("hamil" if a.pregnant else "tidak hamil")

    lines = [
        "TROPICARE – RANGKUMAN SKRINING",
        f"Tanggal   : {when}",
        "Pasien    : " + " · ".join(patient),
        "Tanda bahaya: " + ("; ".join(f.text for f in flags) if flags else "tidak ada"),
        f"Keluhan   : {complaint}",
        f"Pola      : {pattern or '-'}",
        f"Penyerta  : {'; '.join(companions) if companions else '-'}",
        f"{flow.eco_label:<10}: {'; '.join(eco) if eco else 'tidak ada'}",
        f"Obat      : {a.drugs.strip() or '-'}",
    ]
    if "temp" in flow.vitals:
        if no_thermo:
            temp = "tidak diukur (tidak punya termometer)"
        elif a.temp is not None:
            temp = f"{a.temp:.1f} °C"
        else:
            temp = "-"
        lines.append(f"Suhu      : {temp}")
    if "bp" in flow.vitals:
        if no_bp:
            bp = "tidak diukur (tidak punya tensimeter)"
        elif a.bp_sys is not None and a.bp_dia is not None:
            bp = f"{a.bp_sys}/{a.bp_dia} mmHg"
        else:
            bp = "-"
        lines.append(f"Tensi     : {bp}")
    if "glucose" in flow.vitals:
        lines.append(
            f"Gula darah: {_fmt(a.glucose) + ' mg/dL' if a.glucose is not None else '-'}"
        )
    if no_thermo or no_bp:
        lines.append(f"Proksi    : {'; '.join(proxies) if proxies else 'tidak ada'}")
    lines.append(f"Gizi      : {gizi}")
    if flow.measure_waist:
        lines.append(
            f"Lingkar perut: {_fmt(a.waist_cm) + ' cm' if a.waist_cm is not None else '-'}"
        )
    if flow.body_regions:
        lines.append(f"Peta nyeri: {', '.join(body) + pain if body else '-'}")
    lines += [
        f"Foto      : {', '.join(findings) if findings else '-'}",
        f"Lab       : {'; '.join(disease.lab) if disease and disease.lab else '-'}",
        f"Dugaan    : {dugaan}",
        f"Rute      : {r.name} – {r.sub}",
    ]
    return "\n".join(lines)
