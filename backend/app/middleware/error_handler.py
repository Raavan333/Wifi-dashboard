import logging

from fastapi import Request
from fastapi.responses import ORJSONResponse

logger = logging.getLogger(__name__)


async def global_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unhandled Exception",
        exc_info=exc,
    )

    return ORJSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "data": None,
        },
    )