import asyncio

from fastapi import APIRouter

from app.services.dashboard_service import (
    dashboard_service,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


# ============================================================
# COMPLETE DASHBOARD
# ============================================================

@router.get("")
async def get_dashboard():

    (
        summary,
        population,
        connectivity,
        ssid,
        location,
        activity,
        quality,
    ) = await asyncio.gather(
        dashboard_service.get_executive_summary(),
        dashboard_service.get_user_population(),
        dashboard_service.get_connectivity_health(),
        dashboard_service.get_ssid_intelligence(),
        dashboard_service.get_location_overview(),
        dashboard_service.get_user_activity(),
        dashboard_service.get_data_quality(),
    )

    return {
        "executive_summary": summary,
        "user_population": population,
        "connectivity_health": connectivity,
        "ssid_intelligence": ssid,
        "location_overview": location,
        "user_activity": activity,
        "data_quality": quality,
    }


# ============================================================
# INDIVIDUAL SECTIONS
# ============================================================

@router.get("/summary")
async def summary():
    return await dashboard_service.get_executive_summary()


@router.get("/population")
async def population():
    return await dashboard_service.get_user_population()


@router.get("/connectivity")
async def connectivity():
    return await dashboard_service.get_connectivity_health()


@router.get("/ssid")
async def ssid():
    return await dashboard_service.get_ssid_intelligence()


@router.get("/location")
async def location():
    return await dashboard_service.get_location_overview()


@router.get("/activity")
async def activity():
    return await dashboard_service.get_user_activity()


@router.get("/data-quality")
async def data_quality():
    return await dashboard_service.get_data_quality()