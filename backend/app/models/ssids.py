from datetime import datetime
from typing import Optional

from pydantic import Field

from app.models.common import (
    APIModel,
    BarChartResponse,
    PaginationMeta,
)


# ============================================================
# SSID KPI CARD
# ============================================================

class SSIDMetric(APIModel):
    ssid: str

    user_count: int

    user_percentage: float


# ============================================================
# TOP SSID
# ============================================================

class TopSSID(APIModel):
    ssid: str

    user_count: int

    percentage: float


# ============================================================
# FAILURE PRONE SSID
# ============================================================

class FailureSSID(APIModel):
    ssid: str

    failure_count: int


# ============================================================
# INVALID DEVICE SSID
# ============================================================

class InvalidSSID(APIModel):
    ssid: str

    invalid_device_count: int


# ============================================================
# SSID DISTRIBUTION
# ============================================================

class SSIDDistributionItem(APIModel):
    ssid: str

    user_count: int

    percentage: float


# ============================================================
# SSID COMBINATION
# ============================================================

class SSIDCombinationItem(APIModel):
    combination: str

    user_count: int


# Example:
#
# CORP-WIFI
# CORP-WIFI | GUEST
# CORP-WIFI | CORP-5G
# CORP-WIFI | CORP-5G | GUEST


# ============================================================
# SSID DETAIL
# ============================================================

class SSIDDetail(APIModel):
    ssid: str

    total_users: int

    valid_users: int

    invalid_users: int

    success_count: int

    failure_count: int

    success_rate: float

    failure_rate: float


# ============================================================
# SSID LIST ITEM
# ============================================================

class SSIDListItem(APIModel):
    ssid: str

    user_count: int

    valid_user_count: int

    invalid_user_count: int

    success_rate: float


# ============================================================
# SSID TABLE RESPONSE
# ============================================================

class SSIDListResponse(APIModel):
    records: list[SSIDListItem]

    pagination: PaginationMeta


# ============================================================
# SSID USERS
# ============================================================

class SSIDUser(APIModel):
    employee_id: Optional[int]

    user_mac: str

    last_seen_timestamp: Optional[datetime]

    location: Optional[str]

    ux_available: bool

    total_success_count: int

    total_failure_count: int


# ============================================================
# SSID USERS RESPONSE
# ============================================================

class SSIDUsersResponse(APIModel):
    records: list[SSIDUser]

    pagination: PaginationMeta


# ============================================================
# MASTER SSID SECTION RESPONSE
# ============================================================

class SSIDIntelligenceResponse(APIModel):
    total_unique_ssids: int

    most_used_ssid: Optional[TopSSID]

    most_failure_prone_ssid: Optional[FailureSSID]

    most_invalid_ssid: Optional[InvalidSSID]

    user_distribution_chart: BarChartResponse

    ssid_combination_chart: BarChartResponse

    failure_distribution_chart: BarChartResponse


# ============================================================
# SSID FILTER OPTIONS
# ============================================================

class SSIDOption(APIModel):
    ssid: str


class SSIDOptionsResponse(APIModel):
    records: list[SSIDOption] = Field(default_factory=list)