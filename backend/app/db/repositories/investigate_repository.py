from app.db.database import db

from app.db.queries.investigate_queries import (
    BASE_EVENTS_COUNT_QUERY,
    BASE_EVENTS_QUERY,
    EMPLOYEE_PROFILE_QUERY,
    EVENT_TIMELINE_QUERY,
    FILTER_APS_QUERY,
    FILTER_FACILITIES_QUERY,
    FILTER_LOCATIONS_QUERY,
    FILTER_MNEMONICS_QUERY,
    FILTER_SSIDS_QUERY,
    FILTER_STATUSES_QUERY,
    MNEMONIC_DISTRIBUTION_QUERY,
    SEARCH_AP_QUERY,
    SEARCH_EMPLOYEE_QUERY,
    SEARCH_LOCATION_QUERY,
    SEARCH_MAC_QUERY,
    SEARCH_SSID_QUERY,
    STATUS_DISTRIBUTION_QUERY,
    USER_DEVICES_QUERY,
)

from app.models.investigate import (
    InvestigationRequest,
)

from app.utils.filters import QueryBuilder


class InvestigateRepository:

    # ==========================================================
    # EVENT SEARCH
    # ==========================================================

    async def search_events(
        self,
        filters: InvestigationRequest,
    ):

        builder = QueryBuilder()

        builder.in_list(
            "wus.employee_id",
            filters.employee_ids,
        )

        builder.in_list(
            "weh.user_mac",
            filters.user_macs,
        )

        builder.in_list(
            "weh.status",
            filters.statuses,
        )

        builder.in_list(
            "weh.mnemonic",
            filters.mnemonics,
        )

        builder.in_list(
            "weh.facility",
            filters.facilities,
        )

        builder.in_list(
            "wus.location",
            filters.locations,
        )

        builder.in_list(
            "wus.ap_hostname",
            filters.ap_hostnames,
        )

        builder.date_range(
            "weh.appeared_timestamp",
            filters.start_timestamp,
            filters.end_timestamp,
        )

        builder.boolean(
            "wus.ux_available",
            filters.ux_available,
        )

        if filters.valid_users_only:
            builder.valid_users_only()

        query = (
            BASE_EVENTS_QUERY
            + builder.build_where()
            + builder.build_order_by(
                sort_by=filters.sort_by,
                sort_order=filters.sort_order,
                allowed_columns={
                    "appeared_timestamp",
                    "status",
                    "mnemonic",
                    "user_mac",
                },
            )
            + builder.build_pagination(
                filters.page,
                filters.page_size,
            )
        )

        return await db.fetch(
            query,
            *builder.params,
        )

    # ==========================================================
    # EVENT COUNT
    # ==========================================================

    async def count_events(
        self,
        filters: InvestigationRequest,
    ):

        builder = QueryBuilder()

        builder.in_list(
            "wus.employee_id",
            filters.employee_ids,
        )

        builder.in_list(
            "weh.user_mac",
            filters.user_macs,
        )

        builder.in_list(
            "weh.status",
            filters.statuses,
        )

        builder.in_list(
            "weh.mnemonic",
            filters.mnemonics,
        )

        builder.in_list(
            "weh.facility",
            filters.facilities,
        )

        builder.in_list(
            "wus.location",
            filters.locations,
        )

        builder.in_list(
            "wus.ap_hostname",
            filters.ap_hostnames,
        )

        builder.date_range(
            "weh.appeared_timestamp",
            filters.start_timestamp,
            filters.end_timestamp,
        )

        query = (
            BASE_EVENTS_COUNT_QUERY
            + builder.build_where()
        )

        return await db.fetchval(
            query,
            *builder.params,
        )

    # ==========================================================
    # EMPLOYEE PROFILE
    # ==========================================================

    async def get_employee_profile(
        self,
        employee_id: int,
    ):

        query = (
            EMPLOYEE_PROFILE_QUERY
            + """
            WHERE employee_id = $1
            GROUP BY employee_id
            """
        )

        return await db.fetchrow(
            query,
            employee_id,
        )

    # ==========================================================
    # EMPLOYEE DEVICES
    # ==========================================================

    async def get_employee_devices(
        self,
        employee_id: int,
    ):

        query = (
            USER_DEVICES_QUERY
            + """
            WHERE employee_id = $1
            ORDER BY
                last_seen_timestamp DESC
            """
        )

        return await db.fetch(
            query,
            employee_id,
        )

    # ==========================================================
    # MAC DETAILS
    # ==========================================================

    async def get_mac_details(
        self,
        user_mac: str,
    ):

        query = (
            USER_DEVICES_QUERY
            + """
            WHERE user_mac = $1
            """
        )

        return await db.fetchrow(
            query,
            user_mac,
        )

    # ==========================================================
    # EVENT TIMELINE
    # ==========================================================

    async def get_event_timeline(
        self,
        filters: InvestigationRequest,
    ):

        builder = QueryBuilder()

        builder.in_list(
            "user_mac",
            filters.user_macs,
        )

        builder.date_range(
            "appeared_timestamp",
            filters.start_timestamp,
            filters.end_timestamp,
        )

        query = (
            EVENT_TIMELINE_QUERY
            + builder.build_where()
            + """
            GROUP BY activity_date
            ORDER BY activity_date
            """
        )

        return await db.fetch(
            query,
            *builder.params,
        )

    # ==========================================================
    # STATUS DISTRIBUTION
    # ==========================================================

    async def get_status_distribution(
        self,
        filters: InvestigationRequest,
    ):

        builder = QueryBuilder()

        builder.in_list(
            "status",
            filters.statuses,
        )

        query = (
            STATUS_DISTRIBUTION_QUERY
            + builder.build_where()
            + """
            GROUP BY status
            ORDER BY event_count DESC
            """
        )

        return await db.fetch(
            query,
            *builder.params,
        )

    # ==========================================================
    # MNEMONIC DISTRIBUTION
    # ==========================================================

    async def get_mnemonic_distribution(
        self,
        filters: InvestigationRequest,
    ):

        builder = QueryBuilder()

        query = (
            MNEMONIC_DISTRIBUTION_QUERY
            + builder.build_where()
            + """
            GROUP BY mnemonic
            ORDER BY event_count DESC
            LIMIT 25
            """
        )

        return await db.fetch(
            query,
            *builder.params,
        )

    # ==========================================================
    # DROPDOWNS
    # ==========================================================

    async def get_ssid_options(self):
        return await db.fetch(
            FILTER_SSIDS_QUERY
        )

    async def get_status_options(self):
        return await db.fetch(
            FILTER_STATUSES_QUERY
        )

    async def get_mnemonic_options(self):
        return await db.fetch(
            FILTER_MNEMONICS_QUERY
        )

    async def get_location_options(self):
        return await db.fetch(
            FILTER_LOCATIONS_QUERY
        )

    async def get_facility_options(self):
        return await db.fetch(
            FILTER_FACILITIES_QUERY
        )

    async def get_ap_options(self):
        return await db.fetch(
            FILTER_APS_QUERY
        )

    # ==========================================================
    # GLOBAL SEARCH
    # ==========================================================

    async def search_employee(
        self,
        value: str,
    ):
        return await db.fetch(
            SEARCH_EMPLOYEE_QUERY
            + """
            AND employee_id::TEXT ILIKE $1
            LIMIT 20
            """,
            f"%{value}%"
        )

    async def search_mac(
        self,
        value: str,
    ):
        return await db.fetch(
            SEARCH_MAC_QUERY
            + """
            WHERE user_mac ILIKE $1
            LIMIT 20
            """,
            f"%{value}%"
        )


    async def search_ssid(
        self,
        value: str,
    ):
        return await db.fetch(
            SEARCH_SSID_QUERY
            + """
            WHERE ssid ILIKE $1
            LIMIT 20
            """,
            f"%{value}%"
        )

    async def search_ap(
        self,
        value: str,
    ):
        return await db.fetch(
            SEARCH_AP_QUERY
            + """
            AND ap_hostname ILIKE $1
            LIMIT 20
            """,
            f"%{value}%"
        )

    async def search_location(
        self,
        value: str,
    ):
        return await db.fetch(
            SEARCH_LOCATION_QUERY
            + """
            AND location ILIKE $1
            LIMIT 20
            """,
            f"%{value}%"
        )

investigate_repository = InvestigateRepository()