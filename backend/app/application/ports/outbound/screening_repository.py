from collections.abc import Sequence
from typing import Protocol

from app.models import Screening


class ScreeningRepository(Protocol):
    """Outbound port: what the application needs from a screening store."""

    # ponytail: `Screening` is the SQLModel ORM row, so SQLModel leaks into the
    # application layer. Ceiling: the port can't be faked without SQLModel.
    # Upgrade: swap the ORM type for a domain DTO (with the D1c Answers split,
    # wave 3) and map in the adapter.
    def save(self, screening: Screening) -> None: ...

    def list(self, skip: int, limit: int) -> tuple[Sequence[Screening], int]: ...
