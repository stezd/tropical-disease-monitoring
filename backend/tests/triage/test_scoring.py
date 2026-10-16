import math

import pytest

from app.domain.vitals import bp_category
from app.triage.advice import build_result, drug_flags
from app.triage.content import FLOW_IDS, FlowContent, get_content
from app.triage.schemas import Answers, ScoreResult
from app.triage.scoring import ModelEngine, RuleEngine, cvd_risk, features


@pytest.fixture(scope="module")
def content() -> FlowContent:
    return get_content("infection")


@pytest.fixture(scope="module")
def chronic() -> FlowContent:
    return get_content("chronic")


@pytest.fixture(scope="module")
def no_refer(content: FlowContent) -> FlowContent:
    """Infection content with the low-confidence rule off, to test the plain green routes."""
    weights = content.weights.model_copy(update={"refer_below_pct": None})
    return content.model_copy(update={"weights": weights})


def run(content: FlowContent, **kw: object) -> ScoreResult:
    answers = Answers.model_validate({"red_flags": ["none"], **kw})
    return build_result(
        content.flow.id, answers, content, RuleEngine().score(answers, content)
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


def test_high_systolic_upgrades_green_to_yellow(content: FlowContent) -> None:
    r = run(
        content,
        age=50,
        complaint="B",
        pattern="ispa",
        temp=37.0,
        bp_sys=170,
        bp_dia=100,
        nutrition_proxy="normal",
    )
    assert r.route == "yellow"
    assert any("170" in w.text for w in r.warnings)


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


def test_measles_goes_to_special_route(content: FlowContent) -> None:
    """DR no. 6 and 9: mild measles → KUNING KHUSUS (isolation room)."""
    r = run(
        content,
        age=6,
        complaint="D",
        pattern="campak",
        temp=38.5,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "campak"
    assert r.route == "special"
    assert "Isolasi" in r.place


def test_mild_varicella_stays_green(no_refer: FlowContent) -> None:
    r = run(
        no_refer,
        age=9,
        complaint="D",
        pattern="varicella",
        companion=["none"],
        temp=37.8,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "varicella"
    assert r.route == "green"


@pytest.mark.parametrize("sign", ["mata", "nanah"])
def test_severe_varicella_goes_yellow(content: FlowContent, sign: str) -> None:
    """Blisters near the eye or pus → yellow, with a referral note for the doctor."""
    r = run(
        content,
        age=9,
        complaint="D",
        pattern="varicella",
        companion=[sign],
        temp=37.8,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "varicella"
    assert r.route == "yellow"
    assert any(w.icon == "⬆️" for w in r.warnings)
    assert any("Spesialis Kulit/Mata" in w.text for w in r.warnings)
    assert "Spesialis Kulit/Mata" in r.summary


def test_varicella_short_of_breath_goes_red(content: FlowContent) -> None:
    """Varicella pneumonia: short of breath → red (danger sign "napas")."""
    r = run(content, age=9, complaint="D", pattern="varicella", companion=["sesak"])
    assert r.route == "red"
    assert r.top is None
    assert "Sesak napas sangat berat" in r.summary


@pytest.mark.parametrize("pattern", ["lepto", "malaria"])
def test_fever_with_very_yellow_eyes_goes_red(
    content: FlowContent, pattern: str
) -> None:
    """Weil's disease risk: very yellow eyes or skin with fever → red."""
    r = run(content, age=30, complaint="A", pattern=pattern, companion=["kuning"])
    assert r.route == "red"


def test_lepto_without_danger_signs_goes_yellow(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="A",
        pattern="lepto",
        companion=["none"],
        eco=["banjir"],
        temp=38.5,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "lepto"
    assert r.route == "yellow"


def test_hidden_red_flags_need_a_companion(content: FlowContent) -> None:
    hidden = {f.id for f in content.flow.red_flags if not f.listed}
    used = {
        o.red_flag
        for q in content.flow.companions.values()
        for o in q.options
        if o.red_flag
    }
    assert hidden and hidden <= used


def test_varicella_signs_ignored_for_other_patterns(no_refer: FlowContent) -> None:
    r = run(
        no_refer,
        age=20,
        complaint="D",
        pattern="scabies",
        companion=["mata"],
        no_thermo=True,
        nutrition_proxy="normal",
    )
    assert r.route == "green"


def test_red_flag_forces_red_route(content: FlowContent) -> None:
    r = run(content, red_flags=["napas"], complaint="B", pattern="ispa")
    assert r.route == "red"
    assert r.top is None


def test_kkn_papua_vignette_goes_red(content: FlowContent) -> None:
    """DR no. 11: 22 y/o back from Papua, fever every 2 days, now delirious."""
    r = run(
        content,
        red_flags=["otak"],
        who="self",
        age=22,
        sex="L",
        complaint="A",
        pattern="malaria",
        companion=["malaria"],
        eco=["timur"],
        no_thermo=True,
        vital_proxy=["menggigil"],
        nutrition_proxy="longgar",
    )
    assert r.route == "red"
    assert r.top is None


@pytest.mark.parametrize("age", [0, 13, 30, None])
def test_sth_only_for_age_1_to_12(content: FlowContent, age: int | None) -> None:
    """DR no. 3: worm questions only for ages 1–12."""
    r = run(content, age=age, complaint="C", pattern="sth", no_thermo=True)
    assert r.top is None or r.top.id != "sth"


@pytest.mark.parametrize("age", [1, 8, 12])
def test_sth_shown_for_children(content: FlowContent, age: int) -> None:
    r = run(content, age=age, complaint="C", pattern="sth", no_thermo=True)
    assert r.top is not None and r.top.id == "sth"


def test_sth_without_signs_stays_green(no_refer: FlowContent) -> None:
    r = run(
        no_refer,
        age=8,
        complaint="C",
        pattern="sth",
        companion=["none"],
        temp=37.0,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "sth"
    assert r.route == "green"


@pytest.mark.parametrize("sign", ["lesu", "pucat", "buncit"])
def test_sth_with_signs_goes_yellow(content: FlowContent, sign: str) -> None:
    """Child with worms and tiredness, pallor, or a swollen belly → Puskesmas (Hb)."""
    r = run(
        content,
        age=8,
        complaint="C",
        pattern="sth",
        companion=[sign, "pucat"] if sign != "pucat" else [sign],
        temp=37.0,
        nutrition_proxy="normal",
    )
    assert r.top is not None and r.top.id == "sth"
    assert r.route == "yellow"
    notes = [w for w in r.warnings if "hemoglobin" in w.text]
    assert len(notes) == 1


def test_no_thermometer_proxies_in_summary(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="A",
        pattern="malaria",
        no_thermo=True,
        vital_proxy=["menggigil", "nadi"],
        nutrition_proxy="normal",
    )
    assert "Proksi    : Menggigil" in r.summary


def test_drug_flags(content: FlowContent) -> None:
    diare = Answers(complaint="C", pattern="diare", drugs="Loperamide")
    diapet = Answers(complaint="C", pattern="diare", drugs="diapet")
    fever = Answers(complaint="A", pattern="dbd", drugs="ibuprofen 400")
    skin = Answers(complaint="D", pattern="tinea", drugs="Loperamide, ibuprofen")
    swelling = Answers(complaint="E", pattern="filaria", drugs="Amlodipine 5mg")
    cough = Answers(complaint="B", pattern="tbc", drugs="captopril")
    assert drug_flags(diare, content) == ["antidiarrheal"]
    assert drug_flags(diapet, content) == ["antidiarrheal"]
    assert drug_flags(fever, content) == ["nsaid"]
    assert drug_flags(skin, content) == []
    assert drug_flags(swelling, content) == ["amlodipine"]
    assert drug_flags(cough, content) == ["ace_inhibitor"]


def test_drug_popup_in_result(content: FlowContent) -> None:
    r = run(content, complaint="C", pattern="amoeba", drugs="imodium", no_thermo=True)
    assert len(r.drug_popups) == 1
    assert "penghenti mencret" in r.drug_popups[0].text
    assert r.drug_popups[0].level == "y"


def test_drug_popup_levels(content: FlowContent) -> None:
    nsaid = run(content, complaint="A", pattern="dbd", drugs="aspirin", temp=38.5)
    amlo = run(content, complaint="E", pattern="filaria", drugs="amlodipin")
    assert [p.level for p in nsaid.drug_popups] == ["r"]
    assert [p.level for p in amlo.drug_popups] == ["b"]


def test_patient_text_never_says_diagnosis(content: FlowContent) -> None:
    r = run(
        content,
        age=30,
        complaint="D",
        pattern="kusta",
        no_thermo=True,
    )
    patient_text = [r.summary, *r.todo, *r.reasons, *r.cross_checks, *r.analysis_steps]
    patient_text += [w.text for w in r.warnings]
    assert not any("diagnos" in t.lower() for t in patient_text)


@pytest.mark.parametrize("flow_id", FLOW_IDS)
def test_content_never_says_diagnosis(flow_id: str) -> None:
    assert "diagnos" not in get_content(flow_id).model_dump_json().lower()


# Option text that names a disease on purpose. Pending DR (see content/README.md).
# Family history has to name the diseases it asks about (Blueprint Q4).
NAME_EXCEPTIONS = {
    ("kontak", "tbc"),
    ("keturunan", "kencing manis"),
    ("keturunan", "darah tinggi"),
}


@pytest.mark.parametrize("flow_id", FLOW_IDS)
def test_no_disease_names_in_option_text(flow_id: str) -> None:
    content = get_content(flow_id)
    names: set[str] = set()
    for d in content.diseases.values():
        main, _, short = d.name.lower().partition(" (")
        names |= {main, short.rstrip(")")} - {""}
    options = content.flow.all_options()
    found = {(o.id, n) for o in options for n in names if n in o.text.lower()}
    assert found <= NAME_EXCEPTIONS, (
        f"disease names in options: {found - NAME_EXCEPTIONS}"
    )


def test_red_flag_works_in_chronic_path(chronic: FlowContent) -> None:
    r = run(chronic, red_flags=["stroke"], age=60, complaint="G", pattern="hipertensi")
    assert r.route == "red"
    assert r.top is None


def test_chronic_gout(chronic: FlowContent) -> None:
    r = run(
        chronic,
        age=55,
        sex="L",
        complaint="H",
        pattern="gout",
        bp_sys=130,
        bp_dia=85,
        glucose=110,
        height_cm=168,
        weight_kg=80,
        waist_cm=98,
    )
    assert r.top is not None and r.top.id == "gout"
    assert r.route == "yellow"
    assert any("BERPUASA" in w.text for w in r.warnings)
    assert "Tensi     : 130/85 mmHg (meningkat)" in r.summary
    assert "Gula darah sewaktu: 110 mg/dL" in r.summary.splitlines()
    assert "Lingkar perut: 98 cm" in r.summary
    assert "Suhu" not in r.summary
    # The pain map is in both paths now (DR 2026-10-15).
    assert "Peta nyeri: -" in r.summary
    assert "Asam urat : -" in r.summary
    assert r.engine == "rules" and r.fallback is False


def test_chronic_labs_and_joints_in_summary(chronic: FlowContent) -> None:
    r = run(
        chronic,
        age=55,
        complaint="H",
        pattern="gout",
        uric_acid=8.5,
        cholesterol_total=240,
        body=["knee_r", "elbow_l"],
        pain=7,
    )
    rows = {row.key: row.value for row in r.summary_rows}
    assert rows["uric_acid"] == "8.5 mg/dL"
    assert rows["cholesterol_total"] == "240 mg/dL"
    assert rows["body"] == "Siku kiri, Lutut kanan (nyeri 7/10)"
    # Recorded, not scored (weights need ST): same scores as without them.
    plain = run(chronic, age=55, complaint="H", pattern="gout")
    assert r.top is not None and plain.top is not None
    assert r.top.score == plain.top.score


def test_labs_only_where_asked(content: FlowContent) -> None:
    r = run(content, complaint="A", pattern="dbd", uric_acid=8.5)
    assert "uric_acid" not in {row.key for row in r.summary_rows}


@pytest.mark.parametrize(
    ("sys_bp", "dia_bp", "label"),
    [
        (110, 70, "normal"),
        (120, 80, "normal"),
        (121, 80, "meningkat"),
        (139, 89, "meningkat"),
        (135, 90, "tinggi"),
        (140, 80, "tinggi"),
        (160, 100, "tinggi"),
        (161, 95, "sangat tinggi"),
    ],
)
def test_bp_category(sys_bp: int, dia_bp: int, label: str) -> None:
    assert bp_category(sys_bp, dia_bp) == label


@pytest.mark.parametrize(
    ("glucose", "warned"), [(199, False), (200, True), (310, True)]
)
def test_high_random_glucose_warns_without_changing_route(
    chronic: FlowContent, glucose: float, warned: bool
) -> None:
    """GDS ≥ 200 mg/dL (DR 2026-10-15): a yellow notice only."""
    kw = {"age": 50, "complaint": "G", "pattern": "hipertensi", "no_bp": True}
    r = run(chronic, glucose=glucose, **kw)
    plain = run(chronic, **kw)
    notes = [w for w in r.warnings if "Gula darah sewaktu" in w.text]
    assert bool(notes) is warned
    if warned:
        assert notes[0].level == "y" and f"{glucose:g} mg/dL" in notes[0].text
    assert r.route == plain.route
    assert r.top is not None and plain.top is not None
    assert r.top.score == plain.top.score
    rows = {row.key: row.value for row in r.summary_rows}
    suffix = " (≥ 200, tinggi)" if warned else ""
    assert rows["glucose"] == f"{glucose:g} mg/dL{suffix}"


def test_chronic_tengkuk_scores_hypertension_and_lipids(chronic: FlowContent) -> None:
    r = run(chronic, age=50, complaint="G", pattern="hipertensi", no_bp=True)
    assert r.top is not None and r.top.id == "hipertensi"
    assert [o.id for o in r.others][:1] == ["dislipidemia"]
    assert any(w.icon == "🩺" for w in r.warnings)


def test_chronic_without_complaint_is_unknown(chronic: FlowContent) -> None:
    r = run(chronic, age=45, complaint="none", eco=["rokok", "metabolik"], no_bp=True)
    assert r.unknown
    assert r.route == "yellow"
    assert not any("BERPUASA" in w.text for w in r.warnings)
    assert "cek risiko" in r.summary


def test_pregnancy_in_summary(chronic: FlowContent) -> None:
    r = run(chronic, age=30, sex="P", pregnant=True, complaint="none", no_bp=True)
    assert "hamil" in r.summary.split("\n")[2]


def test_province_in_summary(content: FlowContent) -> None:
    r = run(content, complaint="A", pattern="dbd", province="Papua Tengah")
    assert "Provinsi  : Papua Tengah" in r.summary
    assert "Provinsi  : -" in run(content, complaint="A", pattern="dbd").summary


def test_summary_rows_match_text(content: FlowContent) -> None:
    r = run(content, complaint="A", pattern="dbd", province="Papua", temp=38.6)
    rows = {row.key: row for row in r.summary_rows}
    assert rows["province"].value == "Papua"
    assert rows["temp"].value == "38.6 °C"
    assert {"red_flags", "lab", "estimate", "route"} <= rows.keys()
    # The copy text is built from the same rows.
    for row in r.summary_rows:
        assert f"{row.label:<10}: {row.value}" in r.summary


def test_features_are_numeric(content: FlowContent) -> None:
    f = features(Answers(complaint="A", pattern="dbd", no_thermo=True), content)
    assert f["complaint_A"] == 1.0
    assert f["pattern_dbd"] == 1.0
    assert math.isnan(f["temp"])
    assert math.isnan(f["bp_sys"])
    assert f["vital_temp_menggigil"] == 0.0
    assert math.isnan(f["uric_acid"]) and math.isnan(f["cholesterol_total"])
    assert f["body_knee_r"] == 0.0
    assert not any(k.startswith("finding_") for k in f)
    assert all(isinstance(v, float) for v in f.values())
    labs = features(Answers(uric_acid=7.2, cholesterol_total=210), content)
    assert (labs["uric_acid"], labs["cholesterol_total"]) == (7.2, 210.0)


def test_cvd_risk_is_a_skeleton(chronic: FlowContent) -> None:
    assert cvd_risk(Answers(age=50, eco=["rokok"]), chronic) is None


def test_model_engine_is_a_skeleton(content: FlowContent) -> None:
    with pytest.raises(NotImplementedError):
        ModelEngine(None).score(Answers(), content)
