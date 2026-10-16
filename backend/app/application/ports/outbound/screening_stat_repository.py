from dataclasses import dataclass
from datetime import date
from typing import Literal, Protocol

from app.domain.screening_stat import StatRecord

Period = Literal["day", "week"]


@dataclass(frozen=True)
class StatGroup:
    """One group of the summary: period x province x disease x route.

    `count` is None when the group is too small to show (see StatsSummaryUseCase).
    """

    period: date
    province: str | None
    disease: str | None
    route: str
    count: int | None


class ScreeningStatRepository(Protocol):
    """Outbound port: statistics rows without direct identity."""

    def upsert(self, stat: StatRecord) -> None:
        """Insert, or overwrite the row with the same `event_id` (last answer wins)."""
        ...

    def aggregate(
        self,
        period: Period,
        date_from: date | None,
        date_to: date | None,
        flow_id: str | None,
    ) -> list[StatGroup]: ...
