from fastapi import APIRouter, Query

from app.models.investigate import (
    InvestigationRequest,
)

from app.services.investigate_service import (
    investigate_service,
)

router = APIRouter(
    prefix="/investigate",
    tags=["Investigation"],
)


# ==========================================================
# GLOBAL SEARCH
# ==========================================================

@router.get("/search")
async def global_search(
    query: str = Query(
        ...,
        min_length=1,
        description="Global Search Query",
    ),
    page: int = 1,
    page_size: int = 20,
):
    return await investigate_service.global_search(
        query=query,
        page=page,
        page_size=page_size,
    )


# ==========================================================
# FILTER OPTIONS
# ==========================================================

@router.get("/options")
async def get_filter_options():
    return await investigate_service.get_filter_options()


# ==========================================================
# EVENT EXPLORER
# ==========================================================

@router.post("/events")
async def search_events(
    filters: InvestigationRequest,
):
    return await investigate_service.search_events(
        filters
    )


# ==========================================================
# TIMELINE
# ==========================================================

@router.post("/timeline")
async def timeline(
    filters: InvestigationRequest,
):
    return await investigate_service.get_timeline(
        filters
    )


# ==========================================================
# EMPLOYEE DETAILS
# ==========================================================

@router.get("/user/{employee_id}")
async def employee_details(
    employee_id: int,
):
    return await investigate_service.get_employee_overview(
        employee_id
    )


# ==========================================================
# MAC DETAILS
# ==========================================================

@router.get("/mac/{user_mac}")
async def mac_details(
    user_mac: str,
):
    return await investigate_service.get_mac_details(
        user_mac
    )


# ==========================================================
# INVESTIGATION SUMMARY
# ==========================================================

@router.post("/summary")
async def summary(
    filters: InvestigationRequest,
):
    return await investigate_service.get_summary(
        filters
    )