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
        with_coords: bool = False,
    ) -> tuple[Sequence[Facility], int]:
        """Operational facilities in a province, coordinates-first.

        `province_query` accepts a province name ("DKI Jakarta") or dagri code
        ("31"). `kind` accepts a label ("puskesmas", "rs", "apotek") or the raw
        jenis_sarana code ("102", "104", "105"). Set `with_coords` to drop rows
        without latitude/longitude (needed to distance-sort Apotek, most of which
        lack coordinates). Returns (rows, total count).
        """
        ...

    def set_whatsapp(self, satusehat_id: str, wa_number: str | None) -> Facility | None:
        """Set (or clear, with None) a facility's curated WhatsApp number.

        Returns the updated row, or None when no facility has that id. This value
        is deliberately not part of the MSI sync, so re-syncs leave it alone.
        """
        ...

    def list_nearest(
        self,
        latitude: float,
        longitude: float,
        kind: str | None = None,
        limit: int = 3,
    ) -> Sequence[tuple[Facility, float]]:
        """Operational facilities closest to a point, with the distance in km.

        Rows without coordinates are skipped (they cannot be distance-sorted).
        `kind` is the same label or code as `list_by_province`. Facilities that
        are within a short distance of each other are treated as a tie broken by
        data quality, so a reachable, well-recorded facility can edge out a
        marginally closer one. Returns (facility, distance_km), closest first.
        """
        ...
