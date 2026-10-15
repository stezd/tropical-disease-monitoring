import math
from collections.abc import Sequence

from sqlalchemy import ColumnElement, func, or_
from sqlmodel import Session, col, select

from app.models import Facility

_EARTH_KM = 6371.0088

# Two facilities whose distances differ by less than this are treated as a tie,
# broken by data quality instead of metres. Wider than GPS noise, narrower than
# a city block, so genuinely closer facilities still win.
_TIE_KM = 0.5

# Bounding boxes to try before computing exact distances, widening from a city
# to a large part of the country. Keeps the (national) table from being read in
# full on every request.
_BOX_KM = (60.0, 250.0, 1000.0)

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


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km. Good enough to rank nearby facilities."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * _EARTH_KM * math.asin(min(1.0, math.sqrt(a)))


def _quality(facility: Facility) -> int:
    """How complete and trustworthy the contact data is (0–4).

    A phone number scores highest because it is what the call/WhatsApp button
    needs, then a usable address, then MSI's own verified/valid marker.
    """
    score = 2 if facility.phone else 0
    score += 1 if facility.address else 0
    score += 1 if (facility.status_sarana or "").lower() in {"verified", "valid"} else 0
    return score


def _bbox_conditions(lat: float, lon: float, km: float) -> list[ColumnElement[bool]]:
    """Latitude/longitude window of roughly `km` around a point."""
    dlat = km / 111.0
    dlon = km / (111.0 * max(math.cos(math.radians(lat)), 0.01))
    return [
        col(Facility.latitude).between(lat - dlat, lat + dlat),
        col(Facility.longitude).between(lon - dlon, lon + dlon),
    ]


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
        with_coords: bool = False,
    ) -> tuple[Sequence[Facility], int]:
        conditions: list[ColumnElement[bool]] = [
            col(Facility.operational).is_(True),
            _province_condition(province_query),
        ]
        if kind:
            conditions.append(col(Facility.jenis_sarana_kode) == _kind_code(kind))
        if with_coords:
            conditions.append(col(Facility.latitude).isnot(None))
            conditions.append(col(Facility.longitude).isnot(None))

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

    def list_nearest(
        self,
        latitude: float,
        longitude: float,
        kind: str | None = None,
        limit: int = 3,
    ) -> Sequence[tuple[Facility, float]]:
        conditions: list[ColumnElement[bool]] = [
            col(Facility.operational).is_(True),
            col(Facility.latitude).isnot(None),
            col(Facility.longitude).isnot(None),
        ]
        if kind:
            conditions.append(col(Facility.jenis_sarana_kode) == _kind_code(kind))

        rows: list[Facility] = []
        for box_km in _BOX_KM:
            rows = list(
                self._session.exec(
                    select(Facility).where(
                        *conditions, *_bbox_conditions(latitude, longitude, box_km)
                    )
                ).all()
            )
            if len(rows) >= limit:
                break
        if len(rows) < limit:
            # Sparse area, or an island with nothing inside the widest box: read
            # the whole (filtered) table so a far-but-real facility still wins
            # over an empty answer.
            rows = list(self._session.exec(select(Facility).where(*conditions)).all())

        scored: list[tuple[float, int, Facility]] = []
        for row in rows:
            # Already filtered in SQL; re-checked so the types are narrowed.
            if row.latitude is None or row.longitude is None:
                continue
            scored.append(
                (
                    _haversine_km(latitude, longitude, row.latitude, row.longitude),
                    _quality(row),
                    row,
                )
            )
        # Band the distance so near-ties fall back to data quality, then to the
        # true distance. Deterministic: no arbitrary ordering between equals.
        scored.sort(key=lambda s: (int(s[0] // _TIE_KM), -s[1], s[0]))
        return [(row, distance) for distance, _quality_score, row in scored[:limit]]

    def set_whatsapp(self, satusehat_id: str, wa_number: str | None) -> Facility | None:
        row = self._session.exec(
            select(Facility).where(col(Facility.satusehat_id) == satusehat_id)
        ).one_or_none()
        if row is None:
            return None
        row.wa_number = wa_number
        self._session.add(row)
        self._session.commit()
        self._session.refresh(row)
        return row
