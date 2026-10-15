import json

import pytest

from app.triage.content import FLOW_IDS, FlowContent, get_content, raw_content
from app.triage.snapshot import SNAPSHOT_PATH, snapshot

DISEASE_COUNT = {"infection": 19, "chronic": 6}


@pytest.mark.parametrize("flow_id", FLOW_IDS)
def test_content_loads(flow_id: str) -> None:
    content = get_content(flow_id)
    assert content.flow.id == flow_id
    assert len(content.scored_diseases) == DISEASE_COUNT[flow_id]


def test_unknown_flow() -> None:
    with pytest.raises(KeyError):
        get_content("nope")


def test_red_flags_are_shared() -> None:
    """Any danger sign must reach the red screen, whichever path was picked."""
    ids = [{f.id for f in get_content(f).flow.red_flags} for f in FLOW_IDS]
    assert all(i == ids[0] for i in ids)
    assert {"syok", "rabies", "jantung", "stroke", "krisis_ht", "koma_dm"} <= ids[0]


def test_chronic_shows_ptm_red_flags_first() -> None:
    first = [f.id for f in get_content("chronic").flow.red_flags][:4]
    assert first == ["jantung", "stroke", "krisis_ht", "koma_dm"]
    assert get_content("infection").flow.red_flags[0].id == "syok"


def test_bad_red_flag_order_is_rejected() -> None:
    raw = raw_content("chronic")
    raw["flow"]["red_flag_first"] = ["serangan_jantung"]
    with pytest.raises(ValueError, match="serangan_jantung"):
        FlowContent.model_validate(raw)


def test_bad_id_is_rejected() -> None:
    raw = raw_content("infection")
    raw["weights"]["eco"]["banjir"] = {"leptospirosis": 20}
    with pytest.raises(ValueError, match="leptospirosis"):
        FlowContent.model_validate(raw)


def test_bad_option_disease_is_rejected() -> None:
    raw = raw_content("chronic")
    raw["flow"]["patterns"]["G"]["options"][0]["diseases"] = ["hipertensi", "htn"]
    with pytest.raises(ValueError, match="htn"):
        FlowContent.model_validate(raw)


def test_pain_map_step_needs_regions() -> None:
    raw = raw_content("chronic")
    raw["flow"]["body_regions"] = []
    with pytest.raises(ValueError, match="q9"):
        FlowContent.model_validate(raw)


JOINTS = {"knee_r", "knee_l", "elbow_r", "elbow_l", "shoulder_r", "shoulder_l"}


@pytest.mark.parametrize("flow_id", FLOW_IDS)
def test_pain_map_has_joints(flow_id: str) -> None:
    """DR 2026-10-15: knee, elbow, and shoulder on the pain map, in both paths."""
    flow = get_content(flow_id).flow
    assert "q9" in flow.steps
    assert JOINTS <= {r.id for r in flow.body_regions}
    assert "q10" not in flow.steps


def test_chronic_has_optional_labs_step() -> None:
    steps = get_content("chronic").flow.steps
    assert steps[steps.index("q7") + 1] == "labs"
    assert "labs" not in get_content("infection").flow.steps


def test_frontend_snapshot_is_current() -> None:
    """The FE ships a copy of the flow content so the emergency check works offline.

    If this fails, run `bash scripts/generate-client.sh` from the repo root.
    """
    if not SNAPSHOT_PATH.parent.parent.exists():
        pytest.skip("frontend not checked out")
    assert SNAPSHOT_PATH.exists(), "run scripts/generate-client.sh"
    on_disk = json.loads(SNAPSHOT_PATH.read_text("utf-8"))
    assert on_disk == snapshot()
