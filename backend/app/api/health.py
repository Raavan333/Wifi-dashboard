from fastapi import APIRouter

from app.config import get_settings
from app.db.database import db
from app.models.common import HealthCheckResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)

settings = get_settings()


@router.get(
    "",
    response_model=HealthCheckResponse,
)
async def health_check():

    database_status = "connected"

    try:
        await db.fetchval(
            "SELECT 1"
        )
    except Exception:
        database_status = "disconnected"

    return HealthCheckResponse(
        service=settings.APP_NAME,
        version=settings.APP_VERSION,
        status="healthy",
        database=database_status,
    )