"""Text for the "Kak Tropi sedang menebak" screen, the look-alike comparisons, and the meter.

The wording lives in content/<flow>/advice.json (DR); narration only picks the order and
fills in the counts.
"""

from app.domain.answers import Answers
from app.domain.warnings import missing_vitals, no_thermo_text
from app.triage.content import NONE_ID, FlowContent
from app.triage.scoring import Ranked, bmi


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


def pct(share: float) -> int:
    """A 0–1 share as the whole percent the patient sees."""
    return round(share * 100)


def analysis_steps(
    answers: Answers, content: FlowContent, checks: list[tuple[str, str]]
) -> list[str]:
    """Steps on the "Kak Tropi sedang menebak" screen, in the order they appear."""
    steps = content.advice.analysis_steps
    no_thermo, no_bp = missing_vitals(answers, content)
    has_bmi = bmi(answers) is not None
    analysis = [steps.read]
    if no_thermo and steps.no_thermo_fever_pattern and steps.no_thermo_other:
        analysis.append(
            no_thermo_text(
                answers, steps.no_thermo_fever_pattern, steps.no_thermo_other
            )
        )
    if no_bp and steps.no_bp:
        analysis.append(steps.no_bp)
    if not has_bmi:
        analysis.append(steps.no_bmi)
    if not no_thermo and not no_bp and has_bmi:
        analysis.append(steps.vitals_complete)
    analysis.extend(steps.cross_check.format(title=title) for title, _ in checks)
    analysis.append(
        steps.eco.format(count=len([e for e in answers.eco if e != NONE_ID]))
    )
    analysis.append(steps.score)
    analysis.append(steps.route)
    return analysis


def meter(
    ranked: list[Ranked], content: FlowContent, top: Ranked | None
) -> tuple[int, int]:
    """(candidates shown, meter percent) for the mascot's progress bubble."""
    w = content.weights
    candidates = max(1, len([r for r in ranked if r.share >= w.candidate_min_share]))
    meter_pct = min(w.max_display_pct, pct(top.share)) if top else 0
    return candidates, meter_pct
