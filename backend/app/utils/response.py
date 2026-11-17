from typing import Any


def success_response(
    data: Any,
    message: str = "success",
):
    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_response(
    message: str,
):
    return {
        "success": False,
        "message": message,
        "data": None,
    }