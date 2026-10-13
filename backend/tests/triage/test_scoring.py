import math

import pytest

from app.triage.advice import build_result, drug_flags
from app.triage.content import FlowContent, get_content
from app.triage.schemas import Answers, ScoreResult
from app.triage.scoring import ModelEngine, RuleEngine, features


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


def run(content: FlowContent, **kw: object) -> ScoreResult:
    answers = Answers.model_validate({"red_flags": ["none"], **kw})
    return build_result(
        "infection", answers, content, RuleEngine().score(answers, content)
    )


def test_dbd_pattern_goes_yellow(content: FlowContent) -> None:
    r = run(
        content,
        age=25,
        complaint="A",
        pattern="dbd",
        companion=["dbd"],
        temp=39.0,
        height_cm=165,
        weight_kg=60,
        body=["head"],
        pain=5,
    )
    assert r.top is not None and r.top.id == "dbd"
    assert r.route == "yellow"
    assert not r.unknown
    assert r.reasons[0] == "Keluhan utama: Demam & Badan"
    assert "Tunjukkan QR rangkuman ke petugas pendaftaran" in r.todo


def test_low_score_is_unknown_and_yellow(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="E",
        pattern="none",
        no_thermo=True,
        nutrition_proxy="normal",
    )
    assert r.unknown
    assert r.route == "yellow"
    assert r.top is None
    assert "belum dapat ditentukan" in r.summary
    assert r.maps_query == "puskesmas terdekat"


def test_high_fever_upgrades_green_to_yellow(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="B",
        pattern="ispa",
        temp=39.6,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "ispa"
    assert r.route == "yellow"
    assert any(w.icon == "⬆️" for w in r.warnings)


def test_green_route_without_high_fever(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="B",
        pattern="ispa",
        temp=37.0,
        nutrition_proxy="normal",
    )
    assert r.route == "green"
    assert r.nav_label == "Apotek"


def test_tbc_uses_dots_place(content: FlowContent) -> None:
    r = run(
        content,
        age=40,
        complaint="B",
        pattern="tbc",
        companion=["bb", "kms"],
        no_thermo=True,
        nutrition_proxy="longgar",
    )
    assert r.top is not None and r.top.id == "tbc"
    assert r.route == "special"
    assert "DOTS" in r.place


def test_red_flag_forces_red_route(content: FlowContent) -> None:
    r = run(content, red_flags=["napas"], complaint="B", pattern="ispa")
    assert r.route == "red"
    assert r.top is None


def test_child_only_option_ignored_for_adults(content: FlowContent) -> None:
    adult = run(content, age=30, complaint="C", pattern="sth", no_thermo=True)
    child = run(content, age=8, complaint="C", pattern="sth", no_thermo=True)
    assert adult.top is None or adult.top.id != "sth"
    assert child.top is not None and child.top.id == "sth"


def test_drug_flags(content: FlowContent) -> None:
    diare = Answers(complaint="C", pattern="diare", drugs="Loperamide")
    fever = Answers(complaint="A", pattern="dbd", drugs="ibuprofen 400")
    skin = Answers(complaint="D", pattern="tinea", drugs="Loperamide, ibuprofen")
    assert drug_flags(diare, content).antidiarrheal
    assert drug_flags(fever, content).nsaid
    flags = drug_flags(skin, content)
    assert not flags.antidiarrheal and not flags.nsaid


def test_drug_popup_in_result(content: FlowContent) -> None:
    r = run(content, complaint="C", pattern="amoeba", drugs="imodium", no_thermo=True)
    assert len(r.drug_popups) == 1
    assert "obat mampat" in r.drug_popups[0]


def test_patient_text_never_says_diagnosis(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="D",
        pattern="kusta",
        findings=["bercak"],
        no_thermo=True,
    )
    patient_text = [r.summary, *r.todo, *r.reasons, *r.cross_checks, *r.analysis_steps]
    patient_text += [w.text for w in r.warnings]
    assert not any("diagnos" in t.lower() for t in patient_text)


# Option text that names a disease on purpose. Pending DR (see content/README.md).
NAME_EXCEPTIONS = {("mr", "campak"), ("kontak", "tbc")}


def test_no_disease_names_in_option_text(content: FlowContent) -> None:
    names: set[str] = set()
    for d in content.diseases.values():
        main, _, short = d.name.lower().partition(" (")
        names |= {main, short.rstrip(")")} - {""}
    flow = content.flow
    options = [*flow.eco, *flow.findings]
    for q in [*flow.patterns.values(), *flow.companions.values()]:
        options += q.options
    found = {(o.id, n) for o in options for n in names if n in o.text.lower()}
    assert found <= NAME_EXCEPTIONS, (
        f"disease names in options: {found - NAME_EXCEPTIONS}"
    )


def test_features_are_numeric(content: FlowContent) -> None:
    f = features(Answers(complaint="A", pattern="dbd", no_thermo=True), content)
    assert f["complaint_A"] == 1.0
    assert f["pattern_dbd"] == 1.0
    assert math.isnan(f["temp"])
    assert all(isinstance(v, float) for v in f.values())


def test_model_engine_is_a_skeleton(content: FlowContent) -> None:
    with pytest.raises(NotImplementedError):
        ModelEngine(None).score(Answers(), content)
