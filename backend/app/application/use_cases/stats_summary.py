"""Statistics summary with small groups hidden.

A group below `k` screenings has its count set to None, so a rare combination of
province, disease and route cannot point at a person. The rule lives here, not in the
route, so every caller gets it.
"""

from dataclasses import replace
from datetime import date

from app.application.ports.outbound.screening_stat_repository import (
    Period,
    ScreeningStatRepository,
    StatGroup,
)
from app.domain.screening_stat import SMALL_CELL_K


class StatsSummaryUseCase:
    def __init__(self, stats: ScreeningStatRepository, k: int = SMALL_CELL_K) -> None:
        self._stats = stats
        self._k = k

    def execute(
        self,
        period: Period,
        date_from: date | None,
        date_to: date | None,
        flow_id: str | None,
    ) -> list[StatGroup]:
        groups = self._stats.aggregate(period, date_from, date_to, flow_id)
        return [
            replace(g, count=None) if g.count is not None and g.count < self._k else g
            for g in groups
        ]
