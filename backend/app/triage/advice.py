"""Turn scores into what the patient sees: route, warnings, todo list, and summary.

Ported from the prototype's decide(), drugFlags(), crossVal(), adviceFor(), and
summary(). All patient-facing text comes from content/<flow>/advice.json (DR).
"""

from dataclasses import dataclass

from app.triage.content import NONE_ID, FlowContent, Option, RouteId
from app.triage.schemas import Answers, RankedDisease, ScoreResult, Warning
from app.triage.scoring import ScoreBreakdown, bmi, nutrition

JOINT_REGIONS = {"wrist_r", "wrist_l", "ankle_r", "ankle_l"}


@dataclass
class DrugFlags:
    antidiarrheal: bool
    nsaid: bool


def drug_flags(answers: Answers, content: FlowContent) -> DrugFlags:
    drugs = content.advice.drugs
    text = answers.drugs.lower()

    def mentions(keywords: list[str]) -> bool:
        return any(k.lower() in text for k in keywords)

    return DrugFlags(
        antidiarrheal=mentions(drugs.antidiarrheal.keywords)
        and answers.pattern in drugs.antidiarrheal.patterns,
        nsaid=mentions(drugs.nsaid.keywords)
        and answers.complaint in drugs.nsaid.complaints,
    )


def red_flags(answers: Answers) -> list[str]:
    return [f for f in answers.red_flags if f != NONE_ID]


def _fmt(n: float) -> str:
    return f"{n:g}"


def _pct(share: float) -> int:
    return round(share * 100)


def _no_thermo_text(answers: Answers, fever_pattern: str, other: str) -> str:
    return fever_pattern if answers.complaint == "A" else other


def cross_checks(
    answers: Answers, content: FlowContent, s: dict[str, float]
) -> list[tuple[str, str]]:
    """(title, text) for each pair of look-alike diseases worth comparing."""
    cc = content.advice.cross_checks
    c = answers.complaint
    pairs = [
        (cc.tifoid_dbd, "tifoid", "dbd", c in ("A", "C")),
        (cc.kusta_tinea, "kusta", "tinea", c == "D"),
        (cc.diare_amoeba, "amoeba", "diare", c == "C"),
    ]
    out = []
    for check, first, second, by_complaint in pairs:
        a, b = s.get(first, 0), s.get(second, 0)
        if by_complaint or (a > 0 and b > 0):
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
        t = answers.temp
        if (
            route == "green"
            and not answers.no_thermo
            and t is not None
            and t >= w.high_fever_upgrade
        ):
            route = "yellow"
            notes.append(advice.warnings.route_upgraded.format(temp=f"{t:.1f}"))

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
    df = drug_flags(answers, content)
    nut = nutrition(answers, content)
    t = answers.temp
    body = set(answers.body)
    warns: list[Warning] = []
    if df.antidiarrheal:
        warns.append(
            Warning(level="y", icon="💊", text=advice.drugs.antidiarrheal.result)
        )
    if df.nsaid:
        warns.append(Warning(level="y", icon="💊", text=advice.drugs.nsaid.result))
    chik = w.chik_chronic_warning
    if (
        body & JOINT_REGIONS
        and answers.pain is not None
        and answers.pain >= chik.pain_from
        and b.scores.get("chik", 0) >= chik.min_score
    ):
        warns.append(Warning(level="y", icon="🦴", text=advice.warnings.chik_chronic))
    if (
        nut == "obes"
        and b.scores.get("malaria", 0) >= w.malaria_obese_warning_min_score
    ):
        warns.append(Warning(level="r", icon="⚠️", text=advice.warnings.malaria_obese))
    if not answers.no_thermo and t is not None and t >= w.high_fever_upgrade:
        warns.append(
            Warning(
                level="r",
                icon="🌡️",
                text=advice.warnings.high_fever.format(temp=f"{t:.1f}"),
            )
        )
    warns.extend(Warning(level="b", icon="⬆️", text=n) for n in notes)
    if answers.no_thermo:
        warns.append(
            Warning(
                level="b",
                icon="🌡️",
                text=_no_thermo_text(
                    answers,
                    advice.warnings.no_thermo_fever_pattern,
                    advice.warnings.no_thermo_other,
                ),
            )
        )
    if bmi(answers) is None:
        warns.append(Warning(level="b", icon="🤖", text=advice.warnings.no_bmi))

    drug_popups = []
    if df.antidiarrheal:
        drug_popups.append(advice.drugs.antidiarrheal.popup)
    if df.nsaid:
        drug_popups.append(advice.drugs.nsaid.popup)

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
    if answers.no_thermo:
        analysis.append(
            _no_thermo_text(
                answers, steps.no_thermo_fever_pattern, steps.no_thermo_other
            )
        )
    if bmi(answers) is None:
        analysis.append(steps.no_bmi)
    if not answers.no_thermo and bmi(answers) is not None:
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
    pattern_q = flow.patterns.get(a.complaint or "")
    pattern = label(pattern_q.options, a.pattern) if pattern_q else None
    companion_q = flow.companions.get(a.complaint or "")
    companions = (
        [o.text for o in companion_q.options if o.id in a.companion and o.id != NONE_ID]
        if companion_q
        else []
    )
    eco = [o.reason or o.text for o in flow.eco if o.id in a.eco and o.id != NONE_ID]
    flags = [f for f in flow.red_flags if f.id in a.red_flags]
    b = bmi(a)
    if a.no_thermo:
        temp = "tidak diukur (tidak punya termometer)"
    elif a.temp is not None:
        temp = f"{a.temp:.1f} °C"
    else:
        temp = "-"
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

    lines = [
        "TROPICARE – RANGKUMAN SKRINING",
        f"Tanggal   : {when}",
        "Pasien    : "
        + " · ".join(
            [
                label(flow.who, a.who) or "-",
                f"{a.age} th" if a.age is not None else "-",
                label(flow.sex, a.sex) or "-",
            ]
        ),
        "Tanda bahaya: " + ("; ".join(f.text for f in flags) if flags else "tidak ada"),
        f"Keluhan   : {cluster.name if cluster else '-'}",
        f"Pola      : {pattern or '-'}",
        f"Penyerta  : {'; '.join(companions) if companions else '-'}",
        f"Ekologi   : {'; '.join(eco) if eco else 'tidak ada'}",
        f"Obat      : {a.drugs.strip() or '-'}",
        f"Suhu      : {temp}",
        f"Gizi      : {gizi}",
        f"Peta nyeri: {', '.join(body) + pain if body else '-'}",
        f"Foto      : {', '.join(findings) if findings else '-'}",
        f"Lab       : {'; '.join(disease.lab) if disease and disease.lab else '-'}",
        f"Dugaan    : {dugaan}",
        f"Rute      : {r.name} – {r.sub}",
    ]
    return "\n".join(lines)
