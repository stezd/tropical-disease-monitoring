"""Load and validate quiz content from app/triage/content/<flow_id>/*.json.

DR and ST edit the JSON. This module checks that every ID used by one file exists
in the others, so a typo fails at startup and in tests instead of silently
giving wrong scores.

Red flags are shared by every flow (content/red_flags.json): any danger sign must
reach the red screen, whichever path the patient picked.
"""

import json
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import Any, Literal, Self

from pydantic import BaseModel, model_validator

CONTENT_DIR = Path(__file__).parent / "content"
FLOW_IDS = ("infection", "chronic")

RouteId = Literal["green", "yellow", "special", "red"]
WarningLevel = Literal["y", "r", "b"]
StepId = Literal["who", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"]
Vital = Literal["temp", "bp", "glucose"]
NONE_ID = "none"

# Higher = more urgent. Yellow and special are the same level ("minimal kuning").
ROUTE_LEVEL: dict[str, int] = {"green": 0, "yellow": 1, "special": 1, "red": 2}


class Option(BaseModel):
    id: str
    emoji: str
    text: str
    detail: str | None = None
    reason: str | None = None
    disease: str | None = None
    # Several diseases for one option (e.g. a photo finding). Overrides `disease`.
    diseases: list[str] = []
    child_only: bool = False
    # Inclusive age range in years. None = no limit.
    age_min: int | None = None
    age_max: int | None = None
    # Picking this option raises the route to at least this level.
    min_route: RouteId | None = None
    wide: bool = False

    def targets(self, default: str | None = None) -> list[str]:
        """Diseases this option adds points to. Patterns pass their own ID as default."""
        if self.diseases:
            return self.diseases
        if self.disease:
            return [self.disease]
        return [default] if default and default != NONE_ID else []


class RedFlag(BaseModel):
    id: str
    emoji: str
    text: str
    detail: str
    label: str
    condition: str
    facility: str
    first_aid: str | None = None
    # What not to do on the way to hospital (DR no. 19, "DON'T").
    dont: str | None = None


class Cluster(BaseModel):
    id: str
    emoji: str
    name: str
    sub: str
    members: list[str]


class Question(BaseModel):
    title: str
    options: list[Option]
    # Companion questions: show only after one of these patterns. None = always.
    patterns: list[str] | None = None


class StepText(BaseModel):
    """Per-flow wording for a quiz step. Empty fields keep the front end's default."""

    tab: str | None = None
    say: str | None = None
    title: str | None = None
    hint: str | None = None


class Stage(BaseModel):
    emoji: str
    name: str


class BodyRegion(BaseModel):
    id: str
    name: str


class PainFace(BaseModel):
    value: int
    emoji: str
    label: str


class RouteInfo(BaseModel):
    name: str
    sub: str
    emoji: str
    color_from: str
    color_to: str
    place: str
    maps_query: str
    nav_label: str


class Flow(BaseModel):
    id: str
    title: str
    child_age_limit: int
    # Quiz steps in order. "q3"/"q4" are skipped when the complaint has no question.
    steps: list[StepId]
    step_text: dict[StepId, StepText] = {}
    stages: list[Stage]
    who: list[Option]
    sex: list[Option]
    # Ask women from this age whether they are pregnant (Blueprint Q1). None = never.
    pregnancy_from_age: int | None = None
    # Ask for the province (location or picked) in step "who". Goes to MedGemma.
    ask_province: bool = False
    red_flags: list[RedFlag]
    # Red flag IDs shown first in this flow; the rest keep the order of red_flags.json.
    # Order only: every flow still shows every red flag.
    red_flag_first: list[str] = []
    red_maps: dict[str, str]
    clusters: list[Cluster]
    # Lets the patient answer "no complaint" in step q2 (chronic risk check).
    allow_no_complaint: bool = False
    patterns: dict[str, Question]
    companions: dict[str, Question]
    eco: list[Option]
    # Label for the eco answers in the summary.
    eco_label: str = "Ekologi"
    drug_chips: list[str]
    # Measurements in step q7, and the stand-in questions when there is no device.
    vitals: list[Vital]
    vital_proxies: dict[Vital, list[Option]] = {}
    measure_waist: bool = False
    nutrition_proxies: list[Option]
    body_regions: list[BodyRegion]
    pain_faces: list[PainFace]
    findings: list[Option]
    routes: dict[RouteId, RouteInfo]

    @model_validator(mode="after")
    def _order_red_flags(self) -> Self:
        known = {f.id for f in self.red_flags}
        unknown = [i for i in self.red_flag_first if i not in known]
        if unknown:
            raise ValueError(f"flow.red_flag_first: unknown id {unknown}")
        rank = {i: n for n, i in enumerate(self.red_flag_first)}
        self.red_flags.sort(key=lambda f: rank.get(f.id, len(rank)))
        return self

    def all_options(self) -> list[Option]:
        out = [*self.eco, *self.findings, *self.nutrition_proxies]
        for q in [*self.patterns.values(), *self.companions.values()]:
            out += q.options
        for opts in self.vital_proxies.values():
            out += opts
        return out


class Disease(BaseModel):
    name: str
    emoji: str
    route: RouteId
    lab: list[str]
    care: list[str]
    place: str | None = None
    maps_query: str | None = None
    # False = only reachable through a red flag (rabies), never scored.
    scored: bool = True


class DrugRule(BaseModel):
    """Fires when the drug text has a keyword and the answers match.

    `patterns` / `complaints`: the answer must be one of them (empty = any).
    """

    keywords: list[str]
    patterns: list[str] = []
    complaints: list[str] = []
    level: WarningLevel = "y"
    icon: str = "💊"
    popup: str
    result: str


class Warnings(BaseModel):
    """Wording for "Catatan penting". Empty = the warning is not used in this flow."""

    chik_chronic: str | None = None
    malaria_obese: str | None = None
    high_fever: str | None = None
    route_upgraded: str | None = None
    route_upgraded_bp: str | None = None
    route_upgraded_sign: str = "Kondisi dinaikkan ke SEDANG karena ada tanda: {sign}."
    no_thermo_fever_pattern: str | None = None
    no_thermo_other: str | None = None
    no_bp: str | None = None
    no_bmi: str


class Todo(BaseModel):
    green_before: list[str]
    yellow_unknown: list[str]
    yellow_after: list[str]
    special_before: list[str]


class CrossCheck(BaseModel):
    """Two look-alike diseases. Shown for these complaints, or when both score."""

    first_id: str
    second_id: str
    complaints: list[str]
    title: str
    text: str
    first: str
    second: str


class AnalysisSteps(BaseModel):
    read: str
    no_thermo_fever_pattern: str | None = None
    no_thermo_other: str | None = None
    no_bp: str | None = None
    no_bmi: str
    vitals_complete: str
    cross_check: str
    eco: str
    findings: str
    score: str
    route: str


class RouteNote(BaseModel):
    level: WarningLevel
    icon: str
    text: str


class Advice(BaseModel):
    drugs: dict[str, DrugRule] = {}
    warnings: Warnings
    # Extra notes on every result with this route (e.g. fasting before PTM lab tests).
    route_notes: dict[RouteId, list[RouteNote]] = {}
    todo: Todo
    cross_checks: list[CrossCheck] = []
    analysis_steps: AnalysisSteps


class Fever(BaseModel):
    min_temp: float
    points: dict[str, float]
    silent_points: dict[str, float] = {}
    reason: str


class Nutrition(BaseModel):
    bmi_thin_below: float
    bmi_obese_from: float
    thin: dict[str, float]
    obese: dict[str, float]
    thin_reason_bmi: str
    thin_reason_proxy: str
    obese_reason: str


class JointRule(BaseModel):
    regions: list[str]
    disease: str
    points: float
    points_high_pain: float
    high_pain_from: int
    reason: str


class BodyRule(BaseModel):
    any: list[str]
    points: dict[str, float]
    reason: str


class AsymmetryRule(BaseModel):
    right: list[str]
    left: list[str]
    points: dict[str, float]
    reason: str


class BodyWeights(BaseModel):
    joints: JointRule
    rules: list[BodyRule]
    asymmetry: AsymmetryRule


class ChikChronicWarning(BaseModel):
    pain_from: int
    min_score: float


class Weights(BaseModel):
    """Points and thresholds (ST). Sections left out score nothing in this flow."""

    complaint_base: float
    complaint_reason: str
    pattern: float
    companion: float
    finding: float
    eco: dict[str, dict[str, float]]
    province: dict[str, dict[str, float]] = {}
    fever: Fever | None = None
    nutrition: Nutrition
    body: BodyWeights | None = None
    softmax_temperature: float
    candidate_min_share: float
    max_display_pct: int
    low_score_threshold: float
    # Route rules: measured temp from / systolic above this raises green to yellow.
    high_fever_upgrade: float | None = None
    bp_upgrade_above: float | None = None
    chik_chronic_warning: ChikChronicWarning | None = None
    malaria_obese_warning_min_score: float | None = None


class FlowContent(BaseModel):
    flow: Flow
    diseases: dict[str, Disease]
    advice: Advice
    weights: Weights

    @property
    def scored_diseases(self) -> list[str]:
        return [k for k, d in self.diseases.items() if d.scored]

    @model_validator(mode="after")
    def _check_ids(self) -> Self:
        problems: list[str] = []
        scored = set(self.scored_diseases)
        clusters = {c.id for c in self.flow.clusters}
        regions = {r.id for r in self.flow.body_regions}
        eco = {o.id for o in self.flow.eco}

        def need(ids: Iterable[str | None], known: set[str], where: str) -> None:
            for i in ids:
                if i not in known:
                    problems.append(f"{where}: unknown id {i!r}")

        patterns = {o.id for q in self.flow.patterns.values() for o in q.options}
        for c in self.flow.clusters:
            need(c.members, scored, f"flow.clusters[{c.id}].members")
        need(list(self.flow.patterns), clusters, "flow.patterns")
        need(list(self.flow.companions), clusters, "flow.companions")
        for cid, q in self.flow.patterns.items():
            for o in q.options:
                need(o.targets(o.id), scored, f"flow.patterns[{cid}]")
        for cid, q in self.flow.companions.items():
            need(q.patterns or [], patterns, f"flow.companions[{cid}].patterns")
            for o in q.options:
                need(o.targets(), scored, f"flow.companions[{cid}]")
        for o in self.flow.findings:
            need(o.targets(), scored, "flow.findings")
        need(list(self.flow.vital_proxies), set(self.flow.vitals), "flow.vital_proxies")
        need(list(self.weights.eco), eco, "weights.eco")
        for k, pts in self.weights.eco.items():
            need(list(pts), scored, f"weights.eco[{k}]")
        for k, pts in self.weights.province.items():
            need(list(pts), scored, f"weights.province[{k}]")
        if fever := self.weights.fever:
            need(list(fever.points), scored, "weights.fever.points")
            need(list(fever.silent_points), scored, "weights.fever")
        need(list(self.weights.nutrition.thin), scored, "weights.nutrition.thin")
        need(list(self.weights.nutrition.obese), scored, "weights.nutrition.obese")
        if body := self.weights.body:
            need(body.joints.regions, regions, "weights.body.joints")
            need([body.joints.disease], scored, "weights.body.joints")
            for r in body.rules:
                need(r.any, regions, "weights.body.rules")
                need(list(r.points), scored, "weights.body.rules")
            need(body.asymmetry.right + body.asymmetry.left, regions, "weights.body")
            need(list(body.asymmetry.points), scored, "weights.body.asymmetry")
        for name, rule in self.advice.drugs.items():
            need(rule.patterns, patterns, f"advice.drugs[{name}].patterns")
            need(rule.complaints, clusters, f"advice.drugs[{name}].complaints")
        for cc in self.advice.cross_checks:
            need([cc.first_id, cc.second_id], scored, "advice.cross_checks")
            need(cc.complaints, clusters, "advice.cross_checks")
        missing_routes = {"green", "yellow", "special", "red"} - set(self.flow.routes)
        if missing_routes:
            problems.append(f"flow.routes: missing {sorted(missing_routes)}")
        if problems:
            raise ValueError("Invalid triage content:\n" + "\n".join(problems))
        return self


def _read(*parts: str) -> Any:
    return json.loads(CONTENT_DIR.joinpath(*parts).read_text(encoding="utf-8"))


def raw_content(flow_id: str) -> dict[str, Any]:
    """The flow's JSON files as dicts, with the shared red flags merged into the flow."""
    return {
        "flow": {**_read(flow_id, "flow.json"), **_read("red_flags.json")},
        "diseases": _read(flow_id, "diseases.json"),
        "advice": _read(flow_id, "advice.json"),
        "weights": _read(flow_id, "weights.json"),
    }


@cache
def get_content(flow_id: str) -> FlowContent:
    """Return validated content for a flow. Raises KeyError for unknown flows."""
    if flow_id not in FLOW_IDS:
        raise KeyError(flow_id)
    return FlowContent.model_validate(raw_content(flow_id))
