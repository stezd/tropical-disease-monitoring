"""Record one finished screening as a statistics row without direct identity.

Re-scores the answers with the configured engine (the AI engine caches by answers, so
this is normally no second model call; a red flag never calls the model), then keeps
only the whitelisted fields from `domain/screening_stat.py`. Who asked is never passed
in: there is no user, IP, or clock time here.
"""

from collections.abc import Callable
from datetime import date, datetime
from uuid import UUID
from zoneinfo import ZoneInfo

from app.application.ports.outbound.screening_stat_repository import (
    ScreeningStatRepository,
)
from app.application.use_cases.score_flow import ScoreFlowUseCase
from app.domain.answers import Answers
from app.domain.screening_stat import to_stat

WIB = ZoneInfo("Asia/Jakarta")


def today_wib() -> date:
    return datetime.now(WIB).date()


class RecordScreeningUseCase:
    def __init__(
        self,
        score: ScoreFlowUseCase,
        stats: ScreeningStatRepository,
        today: Callable[[], date] = today_wib,
    ) -> None:
        self._score = score
        self._stats = stats
        self._today = today

    def execute(self, event_id: UUID, flow_id: str, answers: Answers) -> None:
        scored = self._score.execute_detailed(flow_id, answers, preview=False)
        self._stats.upsert(
            to_stat(answers, scored.result, scored.engine, self._today(), event_id)
        )
