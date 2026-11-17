from asyncpg import Record

from app.db.database import db
from app.db.queries.dashboard_queries import (
    ACTIVE_USERS_TREND_QUERY,
    CONNECTIVITY_HEALTH_QUERY,
    DATA_QUALITY_QUERY,
    DEVICE_DISTRIBUTION_QUERY,
    DURATION_DISTRIBUTION_QUERY,
    EXECUTIVE_SUMMARY_QUERY,
    LOCATION_DISTRIBUTION_QUERY,
    NEW_USERS_TREND_QUERY,
    RECENT_ACTIVITY_QUERY,
    SSID_COMBINATIONS_QUERY,
    SSID_DISTRIBUTION_QUERY,
    SUCCESS_FAILURE_QUERY,
    USER_POPULATION_QUERY,
)


class DashboardRepository:
    """
    Repository responsible only for database access.
    No transformations.
    No business logic.
    """

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    async def get_executive_summary(self) -> Record:
        return await db.fetchrow(
            EXECUTIVE_SUMMARY_QUERY
        )

    async def get_success_failure(self) -> Record:
        return await db.fetchrow(
            SUCCESS_FAILURE_QUERY
        )

    # ==========================================================
    # USER POPULATION
    # ==========================================================

    async def get_user_population(self) -> Record:
        return await db.fetchrow(
            USER_POPULATION_QUERY
        )

    async def get_recent_activity(self) -> Record:
        return await db.fetchrow(
            RECENT_ACTIVITY_QUERY
        )

    async def get_device_distribution(
        self,
    ) -> list[Record]:
        return await db.fetch(
            DEVICE_DISTRIBUTION_QUERY
        )

    # ==========================================================
    # CONNECTIVITY
    # ==========================================================

    async def get_connectivity_health(
        self,
    ) -> Record:
        return await db.fetchrow(
            CONNECTIVITY_HEALTH_QUERY
        )

    # ==========================================================
    # SSID
    # ==========================================================

    async def get_ssid_distribution(
        self,
        limit: int = 10,
    ) -> list[Record]:
        return await db.fetch(
            SSID_DISTRIBUTION_QUERY,
            limit,
        )

    async def get_ssid_combinations(
        self,
        limit: int = 10,
    ) -> list[Record]:
        return await db.fetch(
            SSID_COMBINATIONS_QUERY,
            limit,
        )

    # ==========================================================
    # LOCATION
    # ==========================================================

    async def get_location_distribution(
        self,
        limit: int = 10,
    ) -> list[Record]:
        return await db.fetch(
            LOCATION_DISTRIBUTION_QUERY,
            limit,
        )

    # ==========================================================
    # USER ACTIVITY
    # ==========================================================

    async def get_duration_distribution(
        self,
    ) -> list:
        return await db.fetch(
            DURATION_DISTRIBUTION_QUERY
        )

    async def get_new_users_trend(
        self,
    ) -> list:
        return await db.fetch(
            NEW_USERS_TREND_QUERY
        )

    async def get_active_users_trend(
        self,
    ) -> list:
        return await db.fetch(
            ACTIVE_USERS_TREND_QUERY
        )

    # ==========================================================
    # DATA QUALITY
    # ==========================================================

    async def get_data_quality(
        self,
    ) -> Record:
        return await db.fetchrow(
            DATA_QUALITY_QUERY
        )


dashboard_repository = DashboardRepository()