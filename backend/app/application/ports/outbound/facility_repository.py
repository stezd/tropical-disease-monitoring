from collections.abc import Sequence
from typing import Protocol

from app.models import Facility


class FacilityRepository(Protocol):
    """Outbound port: what the application needs from the facility mirror."""

    # ponytail: `Facility` is the SQLModel ORM row, same trade-off as
    # ScreeningRepository -- SQLModel leaks into the application layer.
    # Upgrade: swap for a domain DTO and map in the adapter.
    def list_by_province(
        self,
        province_query: str,
        kind: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> tuple[Sequence[Facility], int]:
        """Operational facilities in a province, coordinates-first.

        `province_query` accepts a province name ("DKI Jakarta") or dagri code
        ("31"). `kind` accepts a label ("puskesmas", "rs", "apotek") or the raw
        jenis_sarana code ("102", "104", "105"). Returns (rows, total count).
        """
        ...
