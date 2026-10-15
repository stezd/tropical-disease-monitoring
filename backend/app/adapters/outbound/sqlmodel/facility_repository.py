from collections.abc import Sequence

from sqlalchemy import ColumnElement, func, or_
from sqlmodel import Session, col, select

from app.models import Facility

# MSI calls province 34 "Yogyakarta"; the front end calls it "Daerah Istimewa
# Yogyakarta". Both names, and the code, mean the same province.
_YOGYAKARTA_CODE = "34"
_YOGYAKARTA_NAMES = ["Yogyakarta", "Daerah Istimewa Yogyakarta"]

# Facility kind labels the API accepts, mapped to MSI jenis_sarana codes.
_KIND_CODES = {
    "puskesmas": "102",
    "rs": "104",
    "rumah sakit": "104",
    "igd": "104",
    "apotek": "105",
}


def _province_condition(query: str) -> ColumnElement[bool]:
    """Match a province name or dagri code. Case-insensitive for names."""
    q = query.strip()
    if q.isdigit():
        return col(Facility.province_code) == q
    if q.lower() in {name.lower() for name in _YOGYAKARTA_NAMES} or q.lower() == "diy":
        return or_(
            col(Facility.province_code) == _YOGYAKARTA_CODE,
            col(Facility.province_name).in_(_YOGYAKARTA_NAMES),
        )
    return func.lower(col(Facility.province_name)) == q.lower()


def _kind_code(kind: str) -> str:
    """Map a kind label to its jenis_sarana code. Digits pass through.

    An unknown label falls through unchanged, so it matches no row instead of
    silently returning every kind.
    """
    key = kind.strip().lower()
    return _KIND_CODES.get(key, key)


class SqlModelFacilityRepository:
    """SQLModel adapter for the facility outbound port."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def list_by_province(
        self,
        province_query: str,
        kind: str | None = None,
        limit: int = 100,
        skip: int = 0,
    ) -> tuple[Sequence[Facility], int]:
        conditions: list[ColumnElement[bool]] = [
            col(Facility.operational).is_(True),
            _province_condition(province_query),
        ]
        if kind:
            conditions.append(col(Facility.jenis_sarana_kode) == _kind_code(kind))

        count = self._session.exec(
            select(func.count()).select_from(Facility).where(*conditions)
        ).one()
        rows = self._session.exec(
            select(Facility)
            .where(*conditions)
            .order_by(
                col(Facility.latitude).isnot(None).desc(),
                col(Facility.name).asc(),
            )
            .offset(skip)
            .limit(limit)
        ).all()
        return list(rows), count
