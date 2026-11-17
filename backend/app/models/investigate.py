from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.common import (
    APIModel,
    PaginationMeta,
)


# ============================================================
# GLOBAL SEARCH REQUEST
# ============================================================

class GlobalSearchRequest(APIModel):
    query: str = Field(
        min_length=1,
        max_length=255,
    )

    page: int = Field(
        default=1,
        ge=1,
    )

    page_size: int = Field(
        default=50,
        ge=1,
        le=500,
    )


# ============================================================
# ADVANCED FILTER REQUEST
# ============================================================

class InvestigationRequest(APIModel):
    employee_ids: list[int] = Field(default_factory=list)

    user_macs: list[str] = Field(default_factory=list)

    ssids: list[str] = Field(default_factory=list)

    statuses: list[str] = Field(default_factory=list)

    mnemonics: list[str] = Field(default_factory=list)

    facilities: list[str] = Field(default_factory=list)

    locations: list[str] = Field(default_factory=list)

    ap_hostnames: list[str] = Field(default_factory=list)

    ux_available: Optional[bool] = None

    valid_users_only: bool = False

    start_timestamp: Optional[datetime] = None

    end_timestamp: Optional[datetime] = None

    page: int = 1

    page_size: int = 50

    sort_by: Optional[str] = None

    sort_order: str = "desc"


# ============================================================
# INVESTIGATION KPIs
# ============================================================

class InvestigationSummary(APIModel):
    total_devices: int

    total_users: int

    valid_users: int

    invalid_users: int

    success_rate: float

    failure_rate: float

    recovery_rate: float


# ============================================================
# TIMELINE POINT
# ============================================================

class TimelinePoint(APIModel):
    timestamp: datetime

    success_count: int

    failure_count: int

    exclusion_count: int

    appearance_count: int


# ============================================================
# TIMELINE RESPONSE
# ============================================================

class TimelineResponse(APIModel):
    points: list[TimelinePoint]


# ============================================================
# RAW EVENT
# ============================================================

class RawEvent(APIModel):
    id: int

    user_mac: str

    employee_id: Optional[int]

    facility: str

    mnemonic: str

    status: str

    ssid: Optional[str]

    appeared_timestamp: datetime

    elasticsearch_timestamp: datetime

    ap_hostname: Optional[str]

    location: Optional[str]


# ============================================================
# RAW EVENTS RESPONSE
# ============================================================

class RawEventsResponse(APIModel):
    records: list[RawEvent]

    pagination: PaginationMeta


# ============================================================
# EVENT SEQUENCE
# ============================================================

class EventSequenceItem(APIModel):
    appeared_timestamp: datetime

    status: str

    mnemonic: str

    ssid: Optional[str]


# ============================================================
# DEVICE DETAIL
# ============================================================

class DeviceDetail(APIModel):
    user_mac: str

    employee_id: Optional[int]

    total_appearance_count: int

    total_success_count: int

    total_failure_count: int

    total_exclusion_count: int

    first_seen_timestamp: Optional[datetime]

    last_seen_timestamp: Optional[datetime]

    observed_duration: Optional[str]

    ux_available: bool

    location: Optional[str]

    ap_hostname: Optional[str]

    observed_ssids: list[str] = Field(default_factory=list)


# ============================================================
# SEARCH HIT
# ============================================================

class SearchResult(APIModel):
    entity_type: str

    display_value: str

    matched_field: str


# ============================================================
# GLOBAL SEARCH RESPONSE
# ============================================================

class GlobalSearchResponse(APIModel):
    results: list[SearchResult]

    pagination: PaginationMeta


# ============================================================
# FILTER DROPDOWNS
# ============================================================

class FilterOptionsResponse(APIModel):
    ssids: list[str] = Field(default_factory=list)

    statuses: list[str] = Field(default_factory=list)

    mnemonics: list[str] = Field(default_factory=list)

    facilities: list[str] = Field(default_factory=list)

    locations: list[str] = Field(default_factory=list)

    ap_hostnames: list[str] = Field(default_factory=list)