from fastapi import APIRouter, Query

from app.adapters.outbound.sqlmodel.facility_repository import (
    SqlModelFacilityRepository,
)
from app.api.deps import SessionDep
from app.application.ports.outbound.facility_repository import FacilityRepository
from app.models import FacilitiesPublic, FacilityPublic

router = APIRouter(prefix="/facilities", tags=["facilities"])


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
) -> FacilitiesPublic:
    """Operational health facilities in a province.

    Coordinates-first: facilities with latitude and longitude are returned
    first, so the front end can sort by distance using the browser's position
    without round-tripping patient coordinates to the server.
    """
    repo: FacilityRepository = SqlModelFacilityRepository(session)
    rows, count = repo.list_by_province(
        province_query=province, kind=kind, limit=limit, skip=skip
    )
    return FacilitiesPublic(
        data=[FacilityPublic.model_validate(r) for r in rows],
        count=count,
    )
