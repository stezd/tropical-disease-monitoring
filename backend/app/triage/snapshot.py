"""Write the front end's offline copy of the flow content.

The front end fetches content from the API, but keeps this copy so the emergency
check (stage 1) and the red screen work even when the server is down.

Run from backend/: `uv run python -m app.triage.snapshot`
(scripts/generate-client.sh does it for you).
"""

import json
from pathlib import Path
from typing import Any

from app.triage.content import FLOW_IDS, get_content
from app.triage.schemas import flow_public

SNAPSHOT_PATH = (
    Path(__file__).parents[3]
    / "frontend"
    / "src"
    / "features"
    / "triage"
    / "content.snapshot.json"
)


def snapshot() -> dict[str, Any]:
    return {f: flow_public(get_content(f)).model_dump(mode="json") for f in FLOW_IDS}


def main() -> None:
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(snapshot(), ensure_ascii=False, indent=2) + "\n"
    SNAPSHOT_PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
