"""Scoring. Owned by ST.

Two engines share one interface (`ScoringEngine`):

- `RuleEngine` (default): points from content/<flow>/weights.json. Same rules as the
  prototype's `compute()` in docs/TropiCek-Simulasi.html.
- `ModelEngine` (skeleton): for ST's trained model. `features()` already turns answers
  into a flat numeric vector; plug the model in `ModelEngine.score`.

Pick the engine with the TRIAGE_SCORING_ENGINE setting. Route rules, warnings, and the
summary live in advice.py and work with either engine.
"""

import math
from dataclasses import dataclass, field
from typing import Protocol

from app.domain.answers import Answers
from app.triage.content import NONE_ID, FlowContent, Option, Question


@dataclass
class Ranked:
    id: str
    score: float
    # Share of the softmax over all diseases with a positive score (0–1).
    share: float


@dataclass
class ScoreBreakdown:
    scores: dict[str, float]
    # Why each disease got points, in the order the points were added.
    reasons: dict[str, list[str]]
    # Diseases with a positive score, highest first.
    ranked: list[Ranked] = field(default_factory=list)
    # What produced the scores, saved with a screening: "rules", "model", "ai", or
    # "ai-fb:<reason>" when the AI engine fell back to rules. At most 20 characters.
    engine: str = "rules"


class ScoringEngine(Protocol):
    def score(self, answers: Answers, content: FlowContent) -> ScoreBreakdown: ...


def bmi(answers: Answers) -> float | None:
    h, w = answers.height_cm, answers.weight_kg
    if h is None or w is None or not (50 <= h <= 230 and 3 <= w <= 250):
        return None
    return w / (h / 100) ** 2


def nutrition(answers: Answers, content: FlowContent) -> str | None:
    """ "kurus", "obes", "normal", or None. BMI first, then the proxy question."""
    n = content.weights.nutrition
    b = bmi(answers)
    if b is not None:
        return (
            "kurus"
            if b < n.bmi_thin_below
            else "obes"
            if b >= n.bmi_obese_from
            else "normal"
        )
    return {"longgar": "kurus", "gemuk": "obes", "normal": "normal"}.get(
        answers.nutrition_proxy or ""
    )


def is_child(answers: Answers, content: FlowContent) -> bool:
    return answers.age is not None and answers.age < content.flow.child_age_limit


def visible(o: Option, answers: Answers, content: FlowContent) -> bool:
    """Options limited by age only count when the age fits. Unknown age = hidden."""
    if o.child_only and not is_child(answers, content):
        return False
    if o.age_min is None and o.age_max is None:
        return True
    age = answers.age
    return (
        age is not None
        and (o.age_min is None or age >= o.age_min)
        and (o.age_max is None or age <= o.age_max)
    )


def companion_shown(q: Question, answers: Answers) -> bool:
    return q.patterns is None or answers.pattern in q.patterns


def red_flag_ids(answers: Answers, content: FlowContent) -> list[str]:
    """Danger signs picked in step q1, plus picked companion options that are one
    (e.g. very yellow eyes with fever). Any of them means route MERAH."""
    out = [f for f in answers.red_flags if f != NONE_ID]
    q = content.flow.companions.get(answers.complaint or "")
    if q and companion_shown(q, answers):
        for o in q.options:
            if o.red_flag and o.id in answers.companion and o.red_flag not in out:
                out.append(o.red_flag)
    return out


def rank(scores: dict[str, float], temperature: float) -> list[Ranked]:
    positive = [(k, s) for k, s in scores.items() if s > 0]
    z = sum(math.exp(s / temperature) for _, s in positive)
    ranked = [Ranked(k, s, math.exp(s / temperature) / z) for k, s in positive]
    # Stable sort keeps content order for ties, like the prototype.
    return sorted(ranked, key=lambda r: r.score, reverse=True)


@dataclass(frozen=True)
class Contribution:
    """One points award. An immutable fact; accumulation happens afterwards."""

    disease: str
    points: float
    reason: str | None = None


def accumulate(
    contributions: list[Contribution], scored: list[str]
) -> tuple[dict[str, float], dict[str, list[str]]]:
    """Fold contributions into per-disease scores and ordered, de-duplicated reasons.

    Pure: reads only its arguments and returns fresh dicts. Diseases outside `scored`
    are ignored, and each disease's reasons keep the order the contributions were made
    in — both as in the previous mutating implementation.
    """
    scores = {
        d: sum((c.points for c in contributions if c.disease == d), 0.0) for d in scored
    }
    reasons = {
        d: list(
            dict.fromkeys(
                c.reason for c in contributions if c.disease == d and c.reason
            )
        )
        for d in scored
    }
    return scores, reasons


class RuleEngine:
    def score(self, answers: Answers, content: FlowContent) -> ScoreBreakdown:
        w = content.weights
        flow = content.flow
        contrib: list[Contribution] = []

        cluster = next((x for x in flow.clusters if x.id == answers.complaint), None)
        if cluster:
            contrib += [
                Contribution(
                    d, w.complaint_base, w.complaint_reason.format(name=cluster.name)
                )
                for d in cluster.members
            ]
            pattern_q = flow.patterns.get(cluster.id)
            if pattern_q:
                opt = next(
                    (o for o in pattern_q.options if o.id == answers.pattern), None
                )
                if opt and visible(opt, answers, content):
                    contrib += [
                        Contribution(d, w.pattern, opt.reason)
                        for d in opt.targets(opt.id)
                    ]
            companion_q = flow.companions.get(cluster.id)
            if companion_q and companion_shown(companion_q, answers):
                contrib += [
                    Contribution(d, w.companion, o.reason)
                    for o in companion_q.options
                    if o.id in answers.companion
                    for d in o.targets()
                ]

        contrib += [
            Contribution(d, p, o.reason)
            for o in flow.eco
            if o.id in answers.eco and visible(o, answers, content)
            for d, p in w.eco.get(o.id, {}).items()
        ]

        if answers.province:
            # Pending DR + ST. Empty until endemic provinces and weights are approved.
            contrib += [
                Contribution(d, p)
                for d, p in w.province.get(answers.province, {}).items()
            ]

        # Vital proxies, blood pressure, glucose, and waist score nothing until ST sets
        # weights. They are still in the summary and in features().
        t = answers.temp
        fever = w.fever
        if fever and not answers.no_thermo and t is not None and t >= fever.min_temp:
            fever_reason = fever.reason.format(temp=f"{t:.1f}")
            contrib += [
                Contribution(d, p, fever_reason) for d, p in fever.points.items()
            ]
            contrib += [Contribution(d, p) for d, p in fever.silent_points.items()]

        nut = nutrition(answers, content)
        n = w.nutrition
        if nut == "kurus":
            thin_reason = (
                n.thin_reason_bmi if bmi(answers) is not None else n.thin_reason_proxy
            )
            contrib += [Contribution(d, p, thin_reason) for d, p in n.thin.items()]
        elif nut == "obes":
            contrib += [Contribution(d, p, n.obese_reason) for d, p in n.obese.items()]

        if bw := w.body:
            body = set(answers.body)
            pain = answers.pain if answers.pain is not None else 0
            j = bw.joints
            if body & set(j.regions):
                j_points = j.points_high_pain if pain >= j.high_pain_from else j.points
                contrib.append(
                    Contribution(j.disease, j_points, j.reason.format(pain=pain))
                )
            contrib += [
                Contribution(d, p, rule.reason)
                for rule in bw.rules
                if body & set(rule.any)
                for d, p in rule.points.items()
            ]
            asym = bw.asymmetry
            if bool(body & set(asym.right)) != bool(body & set(asym.left)):
                contrib += [
                    Contribution(d, p, asym.reason) for d, p in asym.points.items()
                ]

        contrib += [
            Contribution(d, w.finding, o.reason)
            for o in flow.findings
            if o.id in answers.findings
            for d in o.targets()
        ]

        scores, reasons = accumulate(contrib, content.scored_diseases)
        return ScoreBreakdown(scores, reasons, rank(scores, w.softmax_temperature))


def features(answers: Answers, content: FlowContent) -> dict[str, float]:
    """Flat numeric features for a trained model. One-hot for every option ID.

    Missing values stay missing (NaN) so tree models can handle them, e.g. no
    thermometer or no scale. Keep feature names stable once a model is trained.
    """
    flow = content.flow
    f: dict[str, float] = {
        "age": float(answers.age) if answers.age is not None else math.nan,
        "sex_p": 1.0 if answers.sex == "P" else 0.0 if answers.sex == "L" else math.nan,
        "temp": answers.temp
        if answers.temp is not None and not answers.no_thermo
        else math.nan,
        "bmi": bmi(answers) or math.nan,
        "pain": float(answers.pain) if answers.pain is not None else math.nan,
        "pregnant": _flag(answers.pregnant),
        "bp_sys": _num(None if answers.no_bp else answers.bp_sys),
        "bp_dia": _num(None if answers.no_bp else answers.bp_dia),
        "glucose": _num(answers.glucose),
        "waist": _num(answers.waist_cm),
    }
    for c in flow.clusters:
        f[f"complaint_{c.id}"] = float(answers.complaint == c.id)
    for q in flow.patterns.values():
        for o in q.options:
            if o.id != NONE_ID:
                f[f"pattern_{o.id}"] = float(answers.pattern == o.id)
    for cid, q in flow.companions.items():
        for o in q.options:
            if o.id != NONE_ID:
                f[f"companion_{cid}_{o.id}"] = float(o.id in answers.companion)
    for o in flow.eco:
        if o.id != NONE_ID:
            f[f"eco_{o.id}"] = float(o.id in answers.eco)
    for p in flow.nutrition_proxies:
        f[f"proxy_{p.id}"] = float(answers.nutrition_proxy == p.id)
    for vital, opts in flow.vital_proxies.items():
        for o in opts:
            if o.id != NONE_ID:
                f[f"vital_{vital}_{o.id}"] = float(o.id in answers.vital_proxy)
    for r in flow.body_regions:
        f[f"body_{r.id}"] = float(r.id in answers.body)
    for o in flow.findings:
        if o.id != NONE_ID:
            f[f"finding_{o.id}"] = float(o.id in answers.findings)
    return f


def _num(v: float | None) -> float:
    return float(v) if v is not None else math.nan


def _flag(v: bool | None) -> float:
    return math.nan if v is None else float(v)


def cvd_risk(answers: Answers, content: FlowContent) -> float | None:  # noqa: ARG001
    """10-year heart attack / stroke risk in % for the chronic path. Skeleton for ST.

    Blueprint Tahap 7: Framingham, adapted, from age, waist, BMI, and smoking
    (`"rokok" in answers.eco`). Return None until ST has the formula. When it exists,
    Blueprint puts "Risiko PTM rendah" at < 5 % on the green route (needs DR + ST).
    """
    return None


class ModelEngine:
    """Skeleton for ST's trained model.

    To finish:
    1. Train on `features()` output (e.g. from DR's case cards), save the model file.
    2. Set TRIAGE_SCORING_ENGINE=model and TRIAGE_MODEL_PATH=<file>.
    3. Load it in `__init__`, and in `score` map class scores to disease IDs.
       Return scores on the same scale as the rule engine (0–100-ish) or adjust
       weights.json thresholds (`low_score_threshold`, `softmax_temperature`) to match.
    Keep `reasons` filled (e.g. top feature contributions) for "Kenapa aku menebak ini?".
    """

    def __init__(self, model_path: str | None) -> None:
        self.model_path = model_path

    def score(self, answers: Answers, content: FlowContent) -> ScoreBreakdown:
        raise NotImplementedError(
            "ModelEngine is a skeleton. Set TRIAGE_SCORING_ENGINE=rules until ST plugs in a model."
        )
