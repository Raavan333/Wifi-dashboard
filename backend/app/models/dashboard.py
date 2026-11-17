from typing import List

from pydantic import Field

from app.models.common import (
    APIModel,
    BarChartResponse,
    LineChartResponse,
    MetricCard,
    PieChartResponse,
)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

class ExecutiveSummaryResponse(APIModel):
    metrics: List[MetricCard]

    success_failure_chart: PieChartResponse

    recovery_chart: PieChartResponse


# ============================================================
# USER POPULATION
# ============================================================

class UserPopulationResponse(APIModel):
    metrics: List[MetricCard]

    device_distribution: BarChartResponse


# ============================================================
# CONNECTIVITY HEALTH
# ============================================================

class ConnectivityHealthResponse(APIModel):
    metrics: List[MetricCard]

    success_failure_chart: PieChartResponse

    recovery_chart: PieChartResponse

    outcome_distribution: BarChartResponse


# ============================================================
# SSID INTELLIGENCE
# ============================================================

class SSIDIntelligenceResponse(APIModel):
    metrics: List[MetricCard]

    user_distribution: BarChartResponse

    ssid_combinations: BarChartResponse

    failure_distribution: BarChartResponse


# ============================================================
# LOCATION & AP OVERVIEW
# ============================================================

class LocationOverviewResponse(APIModel):
    metrics: List[MetricCard]

    user_distribution: BarChartResponse

    device_distribution: BarChartResponse


# ============================================================
# USER ACTIVITY & LIFECYCLE
# ============================================================

class UserActivityResponse(APIModel):
    metrics: List[MetricCard]

    duration_distribution: BarChartResponse

    new_user_trend: LineChartResponse

    active_user_trend: LineChartResponse


# ============================================================
# DATA QUALITY
# ============================================================

class DataQualityResponse(APIModel):
    metrics: List[MetricCard]

    classification_chart: PieChartResponse

    completeness_chart: BarChartResponse


# ============================================================
# MASTER DASHBOARD RESPONSE
# ============================================================

class DashboardResponse(APIModel):
    executive_summary: ExecutiveSummaryResponse

    user_population: UserPopulationResponse

    connectivity_health: ConnectivityHealthResponse

    ssid_intelligence: SSIDIntelligenceResponse

    location_overview: LocationOverviewResponse

    user_activity: UserActivityResponse

    data_quality: DataQualityResponse


# ============================================================
# DROPDOWN OPTIONS
# Used by Filters / Investigation Page
# ============================================================

class DashboardFilterOptions(APIModel):
    locations: List[str] = Field(default_factory=list)

    facilities: List[str] = Field(default_factory=list)

    ssids: List[str] = Field(default_factory=list)

    statuses: List[str] = Field(default_factory=list)

    mnemonics: List[str] = Field(default_factory=list)

    ap_hostnames: List[str] = Field(default_factory=list)