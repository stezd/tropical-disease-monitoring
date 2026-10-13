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
    ids = [[f.id for f in get_content(f).flow.red_flags] for f in FLOW_IDS]
    assert all(i == ids[0] for i in ids)
    assert {"syok", "rabies", "jantung", "stroke", "krisis_ht", "koma_dm"} <= set(
        ids[0]
    )


def test_bad_id_is_rejected() -> None:
    raw = raw_content("infection")
    raw["weights"]["eco"]["banjir"] = {"leptospirosis": 20}
    with pytest.raises(ValueError, match="leptospirosis"):
        FlowContent.model_validate(raw)


def test_bad_finding_disease_is_rejected() -> None:
    raw = raw_content("infection")
    raw["flow"]["findings"][0]["diseases"] = ["campak", "measles"]
    with pytest.raises(ValueError, match="measles"):
        FlowContent.model_validate(raw)


def test_frontend_snapshot_is_current() -> None:
    """The FE ships a copy of the flow content so the emergency check works offline.

    If this fails, run `bash scripts/generate-client.sh` from the repo root.
    """
    if not SNAPSHOT_PATH.parent.parent.exists():
        pytest.skip("frontend not checked out")
    assert SNAPSHOT_PATH.exists(), "run scripts/generate-client.sh"
    on_disk = json.loads(SNAPSHOT_PATH.read_text("utf-8"))
    assert on_disk == snapshot()
