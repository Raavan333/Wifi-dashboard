from app.db.database import db

from app.db.queries.analytics_queries import (
    EVENT_TIMELINE_QUERY,
    LOCATION_SUCCESS_RATES_QUERY,
    OUTCOME_DISTRIBUTION_QUERY,
    RECOVERY_ANALYSIS_VALID_USERS_QUERY,
    TOP_FAILURE_APS_QUERY,
    TOP_FAILURE_SSIDS_QUERY,
    TOP_INVALID_SSIDS_QUERY,
)


class AnalyticsRepository:

    # ==========================================================
    # RECOVERY
    # ==========================================================

    async def get_recovery_analysis(self):
        return await db.fetchrow(
            RECOVERY_ANALYSIS_VALID_USERS_QUERY
        )

    # ==========================================================
    # OUTCOMES
    # ==========================================================

    async def get_outcome_distribution(self):
        return await db.fetchrow(
            OUTCOME_DISTRIBUTION_QUERY
        )

    # ==========================================================
    # FAILURE SSIDS
    # ==========================================================

    async def get_top_failure_ssids(
        self,
        limit: int = 10,
    ):
        return await db.fetch(
            TOP_FAILURE_SSIDS_QUERY,
            limit,
        )

    # ==========================================================
    # INVALID SSIDS
    # ==========================================================

    async def get_top_invalid_ssids(
        self,
        limit: int = 10,
    ):
        return await db.fetch(
            TOP_INVALID_SSIDS_QUERY,
            limit,
        )

    # ==========================================================
    # AP ANALYSIS
    # ==========================================================

    async def get_top_failure_aps(
        self,
        limit: int = 10,
    ):
        return await db.fetch(
            TOP_FAILURE_APS_QUERY,
            limit,
        )

    # ==========================================================
    # LOCATION
    # ==========================================================

    async def get_location_success_rates(self):
        return await db.fetch(
            LOCATION_SUCCESS_RATES_QUERY
        )

    # ==========================================================
    # EVENT TIMELINE
    # ==========================================================

    async def get_event_timeline(self):
        return await db.fetch(
            EVENT_TIMELINE_QUERY
        )


analytics_repository = AnalyticsRepository()