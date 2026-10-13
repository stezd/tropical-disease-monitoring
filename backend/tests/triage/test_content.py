import json

import pytest

from app.triage.content import CONTENT_DIR, FLOW_IDS, FlowContent, get_content
from app.triage.snapshot import SNAPSHOT_PATH, snapshot


@pytest.mark.parametrize("flow_id", FLOW_IDS)
def test_content_loads(flow_id: str) -> None:
    content = get_content(flow_id)
    assert content.flow.id == flow_id
    assert len(content.scored_diseases) == 19


def test_unknown_flow() -> None:
    with pytest.raises(KeyError):
        get_content("chronic")


def test_bad_id_is_rejected() -> None:
    raw = {
        name: json.loads(
            (CONTENT_DIR / "infection" / f"{name}.json").read_text("utf-8")
        )
        for name in ("flow", "diseases", "advice", "weights")
    }
    raw["weights"]["eco"]["banjir"] = {"leptospirosis": 20}
    with pytest.raises(ValueError, match="leptospirosis"):
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
