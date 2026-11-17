from typing import Annotated

from fastapi import Depends, Query

from app.models.common import InvestigationFilters


# ============================================================
# PAGINATION DEPENDENCY
# ============================================================

def pagination_dependency(
    page: int = Query(
        default=1,
        ge=1,
        description="Page Number",
    ),
    page_size: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Records Per Page",
    ),
):
    return {
        "page": page,
        "page_size": page_size,
    }


PaginationDep = Annotated[
    dict,
    Depends(pagination_dependency),
]


# ============================================================
# INVESTIGATION FILTERS
# ============================================================

def investigation_filters_dependency(
    filters: InvestigationFilters = Depends(),
):
    return filters


InvestigationFiltersDep = Annotated[
    InvestigationFilters,
    Depends(investigation_filters_dependency),
]