from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.common import (
    APIModel,
    BarChartResponse,
    LineChartResponse,
    PaginationMeta,
)


# ============================================================
# DEVICE SUMMARY
# ============================================================

class UserDeviceSummary(APIModel):
    user_mac: str

    total_appearance_count: int

    total_success_count: int

    total_failure_count: int

    total_exclusion_count: int

    last_event_status: str

    first_seen_timestamp: Optional[datetime]

    last_seen_timestamp: Optional[datetime]

    observed_duration: Optional[str]

    ux_available: bool

    employee_id: Optional[int]

    location: Optional[str]

    ap_hostname: Optional[str]

    observed_ssids: list[str] = Field(default_factory=list)


# ============================================================
# EMPLOYEE DEVICE RECORD
# ============================================================

class EmployeeDevice(APIModel):
    user_mac: str

    success_count: int

    failure_count: int

    last_seen_timestamp: Optional[datetime]

    last_status: str

    ux_available: bool

    ssid_count: int


# ============================================================
# USER OVERVIEW
# ============================================================

class UserOverview(APIModel):
    employee_id: Optional[int]

    total_devices: int

    valid_devices: int

    invalid_devices: int

    total_success_count: int

    total_failure_count: int

    success_rate: float

    recovery_rate: Optional[float]

    first_seen_timestamp: Optional[datetime]

    last_seen_timestamp: Optional[datetime]

    locations: list[str] = Field(default_factory=list)

    ssids: list[str] = Field(default_factory=list)


# ============================================================
# USER TIMELINE EVENT
# ============================================================

class UserTimelinePoint(APIModel):
    timestamp: datetime

    success_count: int

    failure_count: int

    appearance_count: int


# ============================================================
# USER TIMELINE
# ============================================================

class UserTimeline(APIModel):
    chart: LineChartResponse


# ============================================================
# EMPLOYEE SEARCH RESULT
# ============================================================

class EmployeeSearchResult(APIModel):
    employee_id: int

    device_count: int

    valid_device_count: int

    invalid_device_count: int

    last_seen_timestamp: Optional[datetime]


# ============================================================
# MULTI DEVICE USER
# ============================================================

class MultiDeviceUser(APIModel):
    employee_id: int

    device_count: int

    valid_devices: int

    invalid_devices: int

    last_seen_timestamp: Optional[datetime]


# ============================================================
# MULTI DEVICE RESPONSE
# ============================================================

class MultiDeviceUsersResponse(APIModel):
    records: list[MultiDeviceUser]

    pagination: PaginationMeta


# ============================================================
# USER DETAILS RESPONSE
# ============================================================

class UserDetailsResponse(APIModel):
    overview: UserOverview

    devices: list[EmployeeDevice]

    activity_chart: LineChartResponse

    status_distribution: BarChartResponse


# ============================================================
# RECENT USER
# ============================================================

class RecentUser(APIModel):
    employee_id: Optional[int]

    user_mac: str

    location: Optional[str]

    last_seen_timestamp: Optional[datetime]

    last_status: str


# ============================================================
# RECENT USERS RESPONSE
# ============================================================

class RecentUsersResponse(APIModel):
    records: list[RecentUser]