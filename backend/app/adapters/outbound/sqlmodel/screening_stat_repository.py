from dataclasses import asdict
from datetime import date

from sqlalchemy import Date, func, select
from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, col

from app.application.ports.outbound.screening_stat_repository import (
    Period,
    StatGroup,
)
from app.domain.screening_stat import StatRecord
from app.models import ScreeningStat


class SqlModelScreeningStatRepository:
    """SQLModel (Postgres) adapter for the screening statistics port."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert(self, stat: StatRecord) -> None:
        values = asdict(stat)
        stmt = insert(ScreeningStat).values(**values)
        # Same quiz run again (e.g. "Ubah jawaban" after a red flag): overwrite.
        stmt = stmt.on_conflict_do_update(
            index_elements=["event_id"],
            set_={k: v for k, v in values.items() if k != "event_id"},
        )
        self._session.execute(stmt)
        self._session.commit()

    def aggregate(
        self,
        period: Period,
        date_from: date | None,
        date_to: date | None,
        flow_id: str | None,
    ) -> list[StatGroup]:
        day = col(ScreeningStat.day)
        bucket = func.date_trunc("week", day).cast(Date) if period == "week" else day
        stmt = (
            select(
                bucket.label("period"),
                col(ScreeningStat.province),
                col(ScreeningStat.top_disease),
                col(ScreeningStat.route),
                func.count().label("n"),
            )
            .group_by(
                bucket,
                col(ScreeningStat.province),
                col(ScreeningStat.top_disease),
                col(ScreeningStat.route),
            )
            .order_by(bucket)
        )
        if date_from is not None:
            stmt = stmt.where(day >= date_from)
        if date_to is not None:
            stmt = stmt.where(day <= date_to)
        if flow_id is not None:
            stmt = stmt.where(col(ScreeningStat.flow_id) == flow_id)
        return [
            StatGroup(p, prov, dis, route, n)
            for p, prov, dis, route, n in self._session.execute(stmt).all()
        ]
