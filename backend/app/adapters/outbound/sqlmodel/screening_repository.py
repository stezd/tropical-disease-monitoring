from collections.abc import Sequence

from sqlmodel import Session, col, func, select

from app.models import Screening


class SqlModelScreeningRepository:
    """SQLModel adapter for the screening outbound port."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, screening: Screening) -> None:
        self._session.add(screening)
        self._session.commit()

    def list(self, skip: int, limit: int) -> tuple[Sequence[Screening], int]:
        count = self._session.exec(select(func.count()).select_from(Screening)).one()
        rows = self._session.exec(
            select(Screening)
            .order_by(col(Screening.created_at).desc())
            .offset(skip)
            .limit(limit)
        ).all()
        return list(rows), count
