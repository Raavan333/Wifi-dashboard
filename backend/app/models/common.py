from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# SHARED CONFIG
# ============================================================

class APIModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        str_strip_whitespace=True,
    )


# ============================================================
# GENERIC RESPONSE WRAPPER
# ============================================================

T = TypeVar("T")


class ApiResponse(APIModel, Generic[T]):
    success: bool = True
    message: str = "success"
    data: T


# ============================================================
# PAGINATION
# ============================================================

class PaginationParams(APIModel):
    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=50,
        ge=1,
        le=500,
    )


class PaginationMeta(APIModel):
    page: int
    page_size: int
    total_records: int
    total_pages: int


class PaginatedResponse(APIModel, Generic[T]):
    success: bool = True
    message: str = "success"

    records: List[T]

    pagination: PaginationMeta


# ============================================================
# DATE RANGE
# ============================================================

class DateRange(APIModel):
    start_timestamp: Optional[datetime] = None
    end_timestamp: Optional[datetime] = None


# ============================================================
# SORTING
# ============================================================

class SortRequest(APIModel):
    sort_by: Optional[str] = None

    sort_order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
    )


# ============================================================
# INVESTIGATION FILTERS
# ============================================================

class InvestigationFilters(
    PaginationParams,
    SortRequest,
):
    employee_id: Optional[int] = None

    user_mac: Optional[str] = None

    facility: Optional[str] = None

    location: Optional[str] = None

    ssids: Optional[list[str]] = None

    statuses: Optional[list[str]] = None

    mnemonics: Optional[list[str]] = None

    ap_hostname: Optional[str] = None

    ap_mac: Optional[str] = None

    ux_available: Optional[bool] = None

    valid_users_only: bool = False

    start_timestamp: Optional[datetime] = None

    end_timestamp: Optional[datetime] = None


# ============================================================
# GLOBAL SEARCH
# ============================================================

class GlobalSearchRequest(
    PaginationParams,
):
    query: str = Field(
        min_length=1,
        max_length=255,
    )


# ============================================================
# DROPDOWN OPTIONS
# ============================================================

class OptionItem(APIModel):
    label: str
    value: str


# ============================================================
# HEALTH RESPONSE
# ============================================================

class HealthCheckResponse(APIModel):
    service: str
    version: str
    status: str
    database: str


# ============================================================
# SIMPLE COUNT CARDS
# ============================================================

class MetricCard(APIModel):
    title: str

    value: int | float | str

    subtitle: Optional[str] = None

    trend: Optional[float] = None

    trend_direction: Optional[str] = None


# ============================================================
# PIE CHART
# ============================================================

class PieChartItem(APIModel):
    label: str

    value: int

    percentage: float


class PieChartResponse(APIModel):
    title: str

    items: list[PieChartItem]


# ============================================================
# BAR CHART
# ============================================================

class BarChartItem(APIModel):
    label: str

    value: int


class BarChartResponse(APIModel):
    title: str

    items: list[BarChartItem]


# ============================================================
# LINE CHART
# ============================================================

class LineChartItem(APIModel):
    timestamp: datetime

    value: int


class LineChartResponse(APIModel):
    title: str

    items: list[LineChartItem]