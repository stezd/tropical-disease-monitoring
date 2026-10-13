"""Load and validate quiz content from app/triage/content/<flow_id>/*.json.

DR and ST edit the JSON. This module checks that every ID used by one file exists
in the others, so a typo fails at startup and in tests instead of silently
giving wrong scores.
"""

import json
from collections.abc import Iterable
from functools import cache
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator

CONTENT_DIR = Path(__file__).parent / "content"
FLOW_IDS = ("infection",)

RouteId = Literal["green", "yellow", "special", "red"]
NONE_ID = "none"


class Option(BaseModel):
    id: str
    emoji: str
    text: str
    detail: str | None = None
    reason: str | None = None
    disease: str | None = None
    child_only: bool = False
    wide: bool = False


class RedFlag(BaseModel):
    id: str
    emoji: str
    text: str
    detail: str
    label: str
    condition: str
    facility: str
    first_aid: str


class Cluster(BaseModel):
    id: str
    emoji: str
    name: str
    sub: str
    members: list[str]


class Question(BaseModel):
    title: str
    options: list[Option]


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
    stages: list[Stage]
    who: list[Option]
    sex: list[Option]
    red_flags: list[RedFlag]
    red_maps: dict[str, str]
    clusters: list[Cluster]
    patterns: dict[str, Question]
    companions: dict[str, Question]
    eco: list[Option]
    drug_chips: list[str]
    nutrition_proxies: list[Option]
    body_regions: list[BodyRegion]
    pain_faces: list[PainFace]
    findings: list[Option]
    routes: dict[RouteId, RouteInfo]


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
    keywords: list[str]
    patterns: list[str] = []
    complaints: list[str] = []
    popup: str
    result: str


class Drugs(BaseModel):
    antidiarrheal: DrugRule
    nsaid: DrugRule


class Warnings(BaseModel):
    chik_chronic: str
    malaria_obese: str
    high_fever: str
    route_upgraded: str
    no_thermo_fever_pattern: str
    no_thermo_other: str
    no_bmi: str


class Todo(BaseModel):
    green_before: list[str]
    yellow_unknown: list[str]
    yellow_after: list[str]
    special_before: list[str]


class CrossCheck(BaseModel):
    title: str
    text: str
    first: str
    second: str


class CrossChecks(BaseModel):
    tifoid_dbd: CrossCheck
    kusta_tinea: CrossCheck
    diare_amoeba: CrossCheck


class AnalysisSteps(BaseModel):
    read: str
    no_thermo_fever_pattern: str
    no_thermo_other: str
    no_bmi: str
    vitals_complete: str
    cross_check: str
    eco: str
    findings: str
    score: str
    route: str


class Advice(BaseModel):
    drugs: Drugs
    warnings: Warnings
    todo: Todo
    cross_checks: CrossChecks
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
    complaint_base: float
    complaint_reason: str
    pattern: float
    companion: float
    finding: float
    eco: dict[str, dict[str, float]]
    province: dict[str, dict[str, float]] = {}
    fever: Fever
    nutrition: Nutrition
    body: BodyWeights
    softmax_temperature: float
    candidate_min_share: float
    max_display_pct: int
    low_score_threshold: float
    high_fever_upgrade: float
    chik_chronic_warning: ChikChronicWarning
    malaria_obese_warning_min_score: float


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
        diseases = set(self.diseases)
        scored = set(self.scored_diseases)
        clusters = {c.id for c in self.flow.clusters}
        regions = {r.id for r in self.flow.body_regions}
        eco = {o.id for o in self.flow.eco}

        def need(ids: Iterable[str | None], known: set[str], where: str) -> None:
            for i in ids:
                if i not in known:
                    problems.append(f"{where}: unknown id {i!r}")

        for c in self.flow.clusters:
            need(c.members, scored, f"flow.clusters[{c.id}].members")
        need(list(self.flow.patterns), clusters, "flow.patterns")
        need(list(self.flow.companions), clusters, "flow.companions")
        for cid, q in self.flow.patterns.items():
            need(
                [o.id for o in q.options if o.id != NONE_ID],
                scored,
                f"flow.patterns[{cid}]",
            )
        for cid, q in self.flow.companions.items():
            need(
                [o.disease for o in q.options if o.disease],
                scored,
                f"flow.companions[{cid}]",
            )
        need(
            [o.disease for o in self.flow.findings if o.disease],
            scored,
            "flow.findings",
        )
        need(list(self.weights.eco), eco, "weights.eco")
        for k, pts in self.weights.eco.items():
            need(list(pts), scored, f"weights.eco[{k}]")
        for k, pts in self.weights.province.items():
            need(list(pts), scored, f"weights.province[{k}]")
        need(list(self.weights.fever.points), scored, "weights.fever.points")
        need(list(self.weights.fever.silent_points), scored, "weights.fever")
        need(list(self.weights.nutrition.thin), scored, "weights.nutrition.thin")
        need(list(self.weights.nutrition.obese), scored, "weights.nutrition.obese")
        body = self.weights.body
        need(body.joints.regions, regions, "weights.body.joints")
        need([body.joints.disease], scored, "weights.body.joints")
        for r in body.rules:
            need(r.any, regions, "weights.body.rules")
            need(list(r.points), scored, "weights.body.rules")
        need(body.asymmetry.right + body.asymmetry.left, regions, "weights.body")
        need(list(body.asymmetry.points), scored, "weights.body.asymmetry")
        need(self.advice.drugs.antidiarrheal.patterns, diseases, "advice.drugs")
        need(self.advice.drugs.nsaid.complaints, clusters, "advice.drugs")
        missing_routes = {"green", "yellow", "special", "red"} - set(self.flow.routes)
        if missing_routes:
            problems.append(f"flow.routes: missing {sorted(missing_routes)}")
        if problems:
            raise ValueError("Invalid triage content:\n" + "\n".join(problems))
        return self


def _read(flow_id: str, name: str) -> object:
    return json.loads((CONTENT_DIR / flow_id / name).read_text(encoding="utf-8"))


@cache
def get_content(flow_id: str) -> FlowContent:
    """Return validated content for a flow. Raises KeyError for unknown flows."""
    if flow_id not in FLOW_IDS:
        raise KeyError(flow_id)
    return FlowContent.model_validate(
        {
            "flow": _read(flow_id, "flow.json"),
            "diseases": _read(flow_id, "diseases.json"),
            "advice": _read(flow_id, "advice.json"),
            "weights": _read(flow_id, "weights.json"),
        }
    )
