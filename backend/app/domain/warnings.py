""" "Catatan penting" warnings, drug pop-ups, and the shared vital-sign helpers.

Every branch here picks text straight out of content/<flow>/advice.json (DR), so the
order of the checks is part of the screen the patient sees. All patient-facing text
comes from content/<flow>/advice.json (DR).
"""

from app.domain.answers import Answers
from app.triage.content import NONE_ID, FlowContent, RouteId
from app.triage.schemas import Warning
from app.triage.scoring import ScoreBreakdown, bmi, nutrition

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


def missing_vitals(answers: Answers, content: FlowContent) -> tuple[bool, bool]:
    """(no thermometer, no blood pressure meter), only for vitals this flow asks."""
    vitals = content.flow.vitals
    return (
        "temp" in vitals and answers.no_thermo,
        "bp" in vitals and answers.no_bp,
    )


def no_thermo_text(answers: Answers, fever_pattern: str, other: str) -> str:
    """Which wording to use when the patient had no thermometer."""
    return fever_pattern if answers.complaint == "A" else other


def warnings_for(
    answers: Answers,
    content: FlowContent,
    b: ScoreBreakdown,
    route: RouteId,
    unknown: bool,
    flags: list[str],
    notes: list[str],
) -> tuple[list[Warning], list[Warning]]:
    """(warnings, drug pop-ups). `notes` are the route-upgrade notes from route_policy."""
    no_thermo, no_bp = missing_vitals(answers, content)
    t = answers.temp if not no_thermo else None

    fired = drug_flags(answers, content)
    nut = nutrition(answers, content)
    body = set(answers.body)
    w, wn = content.weights, content.advice.warnings
    warns: list[Warning] = []
    for name in fired:
        rule = content.advice.drugs[name]
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
            for n in content.advice.route_notes.get(route, [])
        )
    warns.extend(Warning(level="b", icon="⬆️", text=n) for n in notes)
    if no_thermo and wn.no_thermo_fever_pattern and wn.no_thermo_other:
        warns.append(
            Warning(
                level="b",
                icon="🌡️",
                text=no_thermo_text(
                    answers, wn.no_thermo_fever_pattern, wn.no_thermo_other
                ),
            )
        )
    if no_bp and wn.no_bp:
        warns.append(Warning(level="b", icon="🩺", text=wn.no_bp))
    if bmi(answers) is None:
        warns.append(Warning(level="b", icon="🤖", text=wn.no_bmi))

    drug_popups = [
        Warning(
            level=content.advice.drugs[n].level,
            icon="⚠️",
            text=content.advice.drugs[n].popup,
        )
        for n in fired
    ]
    return warns, drug_popups
