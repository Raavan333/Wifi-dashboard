import asyncio

from app.cache.cache_keys import (
    DASHBOARD_ACTIVITY,
    DASHBOARD_CONNECTIVITY,
    DASHBOARD_DATA_QUALITY,
    DASHBOARD_LOCATION,
    DASHBOARD_POPULATION,
    DASHBOARD_SSID,
    DASHBOARD_SUMMARY,
)
from app.cache.memory_cache import (
    get_cached,
    set_cached,
)
from app.db.repositories.dashboard_repository import (
    dashboard_repository,
)
from app.models.common import (
    BarChartItem,
    BarChartResponse,
    LineChartItem,
    LineChartResponse,
    MetricCard,
    PieChartItem,
    PieChartResponse,
)
from app.models.dashboard import (
    ConnectivityHealthResponse,
    DataQualityResponse,
    ExecutiveSummaryResponse,
    LocationOverviewResponse,
    SSIDIntelligenceResponse,
    UserActivityResponse,
    UserPopulationResponse,
)


class DashboardService:

    # =========================================================
    # EXECUTIVE SUMMARY
    # =========================================================

    async def get_executive_summary(
        self,
    ) -> ExecutiveSummaryResponse:

        cached = get_cached(
            DASHBOARD_SUMMARY
        )

        if cached:
            return cached

        summary = await dashboard_repository.get_executive_summary()

        success_failure = (
            await dashboard_repository.get_success_failure()
        )

        success_count = (
            success_failure["success_count"] or 0
        )

        failure_count = (
            success_failure["failure_count"] or 0
        )

        total = success_count + failure_count

        response = ExecutiveSummaryResponse(
            metrics=[
                MetricCard(
                    title="Total Devices",
                    value=summary["total_devices"],
                ),
                MetricCard(
                    title="Total Users",
                    value=summary["total_users"],
                ),
                MetricCard(
                    title="Valid Users",
                    value=summary["valid_users"],
                ),
                MetricCard(
                    title="Invalid Devices",
                    value=summary["invalid_devices"],
                ),
                MetricCard(
                    title="UX Unavailable",
                    value=summary["ux_unavailable_users"],
                ),
            ],
            success_failure_chart=PieChartResponse(
                title="Success vs Failure",
                items=[
                    PieChartItem(
                        label="Success",
                        value=success_count,
                        percentage=round(
                            success_count * 100 / total,
                            2,
                        ) if total else 0,
                    ),
                    PieChartItem(
                        label="Failure",
                        value=failure_count,
                        percentage=round(
                            failure_count * 100 / total,
                            2,
                        ) if total else 0,
                    ),
                ],
            ),
            recovery_chart=PieChartResponse(
                title="Recovery Analysis",
                items=[],
            ),
        )

        set_cached(
            DASHBOARD_SUMMARY,
            response,
        )

        return response

    # =========================================================
    # USER POPULATION
    # =========================================================

    async def get_user_population(
        self,
    ) -> UserPopulationResponse:

        cached = get_cached(
            DASHBOARD_POPULATION
        )

        if cached:
            return cached

        population, activity, distribution = (
            await asyncio.gather(
                dashboard_repository.get_user_population(),
                dashboard_repository.get_recent_activity(),
                dashboard_repository.get_device_distribution(),
            )
        )

        chart_items = [
            BarChartItem(
                label=row["bucket"],
                value=row["user_count"],
            )
            for row in distribution
        ]

        response = UserPopulationResponse(
            metrics=[
                MetricCard(
                    title="Valid Users",
                    value=population["valid_users"],
                ),
                MetricCard(
                    title="Multi Device Users",
                    value=population["multi_device_users"],
                ),
                MetricCard(
                    title="MACs Last 7 Days",
                    value=activity["macs_last_7_days"],
                ),
                MetricCard(
                    title="MACs Last 30 Days",
                    value=activity["macs_last_30_days"],
                ),
                MetricCard(
                    title="MACs Last 90 Days",
                    value=activity["macs_last_90_days"],
                ),
            ],
            device_distribution=BarChartResponse(
                title="Devices Per User",
                items=chart_items,
            ),
        )

        set_cached(
            DASHBOARD_POPULATION,
            response,
        )

        return response

    # =========================================================
    # CONNECTIVITY HEALTH
    # =========================================================

    async def get_connectivity_health(
        self,
    ) -> ConnectivityHealthResponse:

        cached = get_cached(
            DASHBOARD_CONNECTIVITY
        )

        if cached:
            return cached

        health = (
            await dashboard_repository.get_connectivity_health()
        )

        response = ConnectivityHealthResponse(
            metrics=[
                MetricCard(
                    title="Success Rate",
                    value=health["success_rate"],
                ),
                MetricCard(
                    title="Failure Rate",
                    value=health["failure_rate"],
                ),
            ],
            success_failure_chart=PieChartResponse(
                title="Success vs Failure",
                items=[
                    PieChartItem(
                        label="Success",
                        value=health["total_success"],
                        percentage=float(
                            health["success_rate"]
                        ),
                    ),
                    PieChartItem(
                        label="Failure",
                        value=health["total_failure"],
                        percentage=float(
                            health["failure_rate"]
                        ),
                    ),
                ],
            ),
            recovery_chart=PieChartResponse(
                title="Recovery Analysis",
                items=[],
            ),
            outcome_distribution=BarChartResponse(
                title="Outcome Distribution",
                items=[],
            ),
        )

        set_cached(
            DASHBOARD_CONNECTIVITY,
            response,
        )

        return response

    # =========================================================
    # SSID INTELLIGENCE
    # =========================================================

    async def get_ssid_intelligence(
        self,
    ) -> SSIDIntelligenceResponse:

        cached = get_cached(
            DASHBOARD_SSID
        )

        if cached:
            return cached

        distribution, combinations = (
            await asyncio.gather(
                dashboard_repository.get_ssid_distribution(),
                dashboard_repository.get_ssid_combinations(),
            )
        )

        response = SSIDIntelligenceResponse(
            metrics=[],
            user_distribution=BarChartResponse(
                title="Users Per SSID",
                items=[
                    BarChartItem(
                        label=row["ssid"],
                        value=row["user_count"],
                    )
                    for row in distribution
                ],
            ),
            ssid_combinations=BarChartResponse(
                title="SSID Combinations",
                items=[
                    BarChartItem(
                        label=row["ssid_combination"],
                        value=row["user_count"],
                    )
                    for row in combinations
                ],
            ),
            failure_distribution=BarChartResponse(
                title="SSID Failures",
                items=[],
            ),
        )

        set_cached(
            DASHBOARD_SSID,
            response,
        )

        return response

    # =========================================================
    # LOCATION OVERVIEW
    # =========================================================

    async def get_location_overview(
        self,
    ) -> LocationOverviewResponse:

        cached = get_cached(
            DASHBOARD_LOCATION
        )

        if cached:
            return cached

        locations = (
            await dashboard_repository.get_location_distribution()
        )

        response = LocationOverviewResponse(
            metrics=[],
            user_distribution=BarChartResponse(
                title="Users By Location",
                items=[
                    BarChartItem(
                        label=row["location"],
                        value=row["device_count"],
                    )
                    for row in locations
                ],
            ),
            device_distribution=BarChartResponse(
                title="Devices By Location",
                items=[
                    BarChartItem(
                        label=row["location"],
                        value=row["device_count"],
                    )
                    for row in locations
                ],
            ),
        )

        set_cached(
            DASHBOARD_LOCATION,
            response,
        )

        return response

    # =========================================================
    # USER ACTIVITY
    # =========================================================

    async def get_user_activity(
        self,
    ) -> UserActivityResponse:

        cached = get_cached(
            DASHBOARD_ACTIVITY
        )

        if cached:
            return cached

        (
            duration,
            new_users,
            active_users,
        ) = await asyncio.gather(
            dashboard_repository.get_duration_distribution(),
            dashboard_repository.get_new_users_trend(),
            dashboard_repository.get_active_users_trend(),
        )

        response = UserActivityResponse(
            metrics=[],
            duration_distribution=BarChartResponse(
                title="Observed Duration",
                items=[
                    BarChartItem(
                        label=row["duration_bucket"],
                        value=row["user_count"],
                    )
                    for row in duration
                ],
            ),
            new_user_trend=LineChartResponse(
                title="New Users",
                items=[
                    LineChartItem(
                        timestamp=row["observation_date"],
                        value=row["users"],
                    )
                    for row in new_users
                ],
            ),
            active_user_trend=LineChartResponse(
                title="Active Users",
                items=[
                    LineChartItem(
                        timestamp=row["observation_date"],
                        value=row["users"],
                    )
                    for row in active_users
                ],
            ),
        )

        set_cached(
            DASHBOARD_ACTIVITY,
            response,
        )

        return response

    # =========================================================
    # DATA QUALITY
    # =========================================================

    async def get_data_quality(
        self,
    ) -> DataQualityResponse:

        cached = get_cached(
            DASHBOARD_DATA_QUALITY
        )

        if cached:
            return cached

        data = (
            await dashboard_repository.get_data_quality()
        )

        response = DataQualityResponse(
            metrics=[
                MetricCard(
                    title="Valid Users",
                    value=data["valid_users"],
                ),
                MetricCard(
                    title="Unmapped Users",
                    value=data["unmapped_users"],
                ),
                MetricCard(
                    title="UX Missing",
                    value=data["ux_missing_users"],
                ),
                MetricCard(
                    title="Invalid Devices",
                    value=data["invalid_devices"],
                ),
            ],
            classification_chart=PieChartResponse(
                title="User Classification",
                items=[
                    PieChartItem(
                        label="Valid",
                        value=data["valid_users"],
                        percentage=0,
                    ),
                    PieChartItem(
                        label="Unmapped",
                        value=data["unmapped_users"],
                        percentage=0,
                    ),
                    PieChartItem(
                        label="UX Missing",
                        value=data["ux_missing_users"],
                        percentage=0,
                    ),
                    PieChartItem(
                        label="Invalid",
                        value=data["invalid_devices"],
                        percentage=0,
                    ),
                ],
            ),
            completeness_chart=BarChartResponse(
                title="Data Completeness",
                items=[],
            ),
        )

        set_cached(
            DASHBOARD_DATA_QUALITY,
            response,
        )

        return response


dashboard_service = DashboardService()