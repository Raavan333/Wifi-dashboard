from __future__ import annotations

from functools import wraps
from typing import Any, Callable

from cachetools import TTLCache


# ============================================================
# GLOBAL CACHE
# ============================================================

dashboard_cache = TTLCache(
    maxsize=1024,
    ttl=60,
)


# ============================================================
# GET CACHE
# ============================================================

def get_cached(key: str) -> Any | None:
    return dashboard_cache.get(key)


# ============================================================
# SET CACHE
# ============================================================

def set_cached(
    key: str,
    value: Any,
) -> None:
    dashboard_cache[key] = value


# ============================================================
# DELETE CACHE ENTRY
# ============================================================

def delete_cached(key: str) -> None:
    dashboard_cache.pop(key, None)


# ============================================================
# CLEAR EVERYTHING
# ============================================================

def clear_cache() -> None:
    dashboard_cache.clear()


# ============================================================
# CACHE DECORATOR
# ============================================================

def cache_result(
    ttl_cache: TTLCache = dashboard_cache,
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = (
                f"{func.__module__}:"
                f"{func.__name__}:"
                f"{str(args)}:"
                f"{str(kwargs)}"
            )

            cached = ttl_cache.get(cache_key)

            if cached is not None:
                return cached

            result = await func(*args, **kwargs)

            ttl_cache[cache_key] = result

            return result

        return wrapper

    return decorator