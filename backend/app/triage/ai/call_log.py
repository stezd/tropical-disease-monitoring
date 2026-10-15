"""One JSON line per scoring, for evaluating the user test. Best effort: never raises.

What goes in: request id, flow, mode, model, prompt version, scores from the model and
from RuleEngine, fallback reason, latency, tokens, and (if LOG_FACTS) the fact lines.
What never goes in: name, NIK, BPJS, coordinates, photos, the free-text drug field.
"""

import json
import logging
import threading
from pathlib import Path
from typing import Any

logger = logging.getLogger("app.triage.ai")


class CallLog:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self._lock = threading.Lock()

    def write(self, record: dict[str, Any]) -> None:
        try:
            line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
            if self.path is None:
                logger.info("ai_call %s", line)
                return
            with self._lock:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                with self.path.open("a", encoding="utf-8") as f:
                    f.write(line + "\n")
        except Exception:  # noqa: BLE001 - logging must never break scoring
            logger.exception("could not write AI call log")
