"""Photo analysis. Skeleton, owned by ST (low priority).

The photo step asks the patient to photograph a rash, wound, tongue, or eye. Until a
model exists, `UnavailableAnalyzer` answers `available=False` and the front end keeps
the prototype's simulated step: the patient picks the findings they see.

To plug in a model:
1. Write a class with `analyze(image: bytes, content_type: str) -> list[str]` that
   returns finding IDs from content/<flow>/flow.json `findings` (e.g. "lidah", "cincin").
2. Add its name to TRIAGE_PHOTO_ANALYZER in app/core/config.py and return it from
   `get_analyzer()`.
3. Update the consent text in the front end (photo step) to say the photo goes to our
   server for analysis and is not stored.

Privacy: photos are health data. Never write them to disk, logs, or the database.
"""

from typing import Protocol

from app.core.config import settings

MAX_PHOTO_BYTES = 8 * 1024 * 1024
ALLOWED_TYPES = ("image/jpeg", "image/png", "image/webp", "image/heic", "image/heif")


class PhotoAnalyzer(Protocol):
    available: bool

    def analyze(self, image: bytes, content_type: str) -> list[str]: ...


class UnavailableAnalyzer:
    available = False

    def analyze(self, image: bytes, content_type: str) -> list[str]:  # noqa: ARG002
        return []


def get_analyzer() -> PhotoAnalyzer:
    match settings.TRIAGE_PHOTO_ANALYZER:
        case "none":
            return UnavailableAnalyzer()
