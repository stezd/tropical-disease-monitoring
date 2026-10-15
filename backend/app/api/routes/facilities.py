from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.adapters.outbound.sqlmodel.facility_repository import (
    SqlModelFacilityRepository,
)
from app.api.deps import SessionDep, get_current_active_superuser
from app.application.ports.outbound.facility_repository import FacilityRepository
from app.models import (
    FacilitiesNearestPublic,
    FacilitiesPublic,
    FacilityNearestPublic,
    FacilityPublic,
)

router = APIRouter(prefix="/facilities", tags=["facilities"])


class FacilityNearestRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    kind: str | None = Field(
        default=None,
        description="Facility kind: 'puskesmas' (102), 'rs' (104), 'apotek' (105)",
    )
    limit: int = Field(default=3, ge=1, le=20)


class FacilityWhatsappUpdate(BaseModel):
    wa_number: str | None = Field(
        default=None,
        description="Indonesian mobile number (08… / +62 8…), or null/empty to "
        "clear. Stored in international form (628…).",
    )


def normalize_wa_number(value: str) -> str:
    """Turn a typed Indonesian mobile number into `628…`, or raise ValueError.

    MSI has no WhatsApp field and its `telp` is usually a landline, so a curated
    number must be a mobile: only `08…` / `628…` are accepted. Anything else
    (landline area codes like 021, short codes) is rejected rather than silently
    producing a WhatsApp link that goes nowhere.
    """
    digits = "".join(ch for ch in value if ch.isdigit())
    if digits.startswith("0"):
        digits = f"62{digits[1:]}"
    if not digits.startswith("628") or not 10 <= len(digits) <= 15:
        raise ValueError(
            "Bukan nomor seluler Indonesia yang valid (contoh: 08123456789)."
        )
    return digits


@router.get("/", response_model=FacilitiesPublic)
def list_facilities(
    session: SessionDep,
    province: str = Query(
        ...,
        min_length=2,
        description="Province name or code, e.g. 'DKI Jakarta' or '31'",
    ),
    kind: str | None = Query(
        None,
        description="Facility kind: 'puskesmas' (102), 'rs' (104), 'apotek' (105)",
    ),
    limit: int = Query(100, ge=1, le=500),
    skip: int = Query(0, ge=0),
    with_coords: bool = Query(
        False,
        description="Only facilities that have coordinates (needed to sort by "
        "distance; most Apotek rows lack them)",
    ),
) -> FacilitiesPublic:
    """Operational health facilities in a province.

    Coordinates-first: facilities with latitude and longitude are returned
    first, so the front end can sort by distance using the browser's position
    without round-tripping patient coordinates to the server.
    """
    repo: FacilityRepository = SqlModelFacilityRepository(session)
    rows, count = repo.list_by_province(
        province_query=province,
        kind=kind,
        limit=limit,
        skip=skip,
        with_coords=with_coords,
    )
    return FacilitiesPublic(
        data=[FacilityPublic.model_validate(r) for r in rows],
        count=count,
    )


@router.post("/nearest", response_model=FacilitiesNearestPublic)
def nearest_facilities(
    session: SessionDep,
    body: FacilityNearestRequest,
) -> FacilitiesNearestPublic:
    """The closest operational facilities to a point, nearest first.

    Opt-in proximity path. The default for the app is to rank in the browser
    from the province list, so patient coordinates stay on the device; this
    endpoint exists for cross-province accuracy and is only called when
    `VITE_FACILITIES_SERVER_NEAREST=true`.

    Coordinates are used to compute the answer and are not stored. They travel
    in the request body (not the URL) so they do not land in access logs.
    Facilities roughly the same distance away are ordered by data quality, so a
    reachable, well-documented one can come first.
    """
    repo: FacilityRepository = SqlModelFacilityRepository(session)
    rows = repo.list_nearest(
        latitude=body.latitude,
        longitude=body.longitude,
        kind=body.kind,
        limit=body.limit,
    )
    return FacilitiesNearestPublic(
        data=[
            FacilityNearestPublic(
                **FacilityPublic.model_validate(facility).model_dump(),
                distance_km=round(distance, 2),
            )
            for facility, distance in rows
        ],
        count=len(rows),
    )


@router.put(
    "/{satusehat_id}/whatsapp",
    response_model=FacilityPublic,
    dependencies=[Depends(get_current_active_superuser)],
)
def set_facility_whatsapp(
    satusehat_id: str,
    body: FacilityWhatsappUpdate,
    session: SessionDep,
) -> FacilityPublic:
    """Curate one facility's WhatsApp number (superuser only).

    The mirror has no WhatsApp data, so a human adds the numbers that matter for
    the pilot. The value is not touched by the MSI sync, so it survives re-syncs.
    Send null (or an empty string) to clear it.
    """
    normalized: str | None = None
    if body.wa_number and body.wa_number.strip():
        try:
            normalized = normalize_wa_number(body.wa_number)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
    repo: FacilityRepository = SqlModelFacilityRepository(session)
    row = repo.set_whatsapp(satusehat_id, normalized)
    if row is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    return FacilityPublic.model_validate(row)
