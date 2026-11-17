import asyncio
import math

from app.db.repositories.investigate_repository import (
    investigate_repository,
)

from app.models.common import PaginationMeta

from app.models.investigate import (
    FilterOptionsResponse,
    GlobalSearchResponse,
    InvestigationRequest,
    InvestigationSummary,
    RawEvent,
    RawEventsResponse,
    SearchResult,
    TimelinePoint,
    TimelineResponse,
)


class InvestigateService:

    # ==========================================================
    # RAW EVENT SEARCH
    # ==========================================================

    async def search_events(
        self,
        filters: InvestigationRequest,
    ):

        rows, total_records = await asyncio.gather(
            investigate_repository.search_events(
                filters
            ),
            investigate_repository.count_events(
                filters
            ),
        )

        records = [
            RawEvent(
                id=row["id"],
                user_mac=row["user_mac"],
                employee_id=row["employee_id"],
                facility=row["facility"],
                mnemonic=row["mnemonic"],
                status=row["status"],
                ssid=row["ssid"],
                appeared_timestamp=row["appeared_timestamp"],
                elasticsearch_timestamp=row["elasticsearch_timestamp"],
                location=row["location"],
                ap_hostname=row["ap_hostname"],
            )
            for row in rows
        ]

        total_pages = math.ceil(
            total_records / filters.page_size
        )

        return RawEventsResponse(
            records=records,
            pagination=PaginationMeta(
                page=filters.page,
                page_size=filters.page_size,
                total_records=total_records,
                total_pages=total_pages,
            ),
        )

    # ==========================================================
    # TIMELINE
    # ==========================================================

    async def get_timeline(
        self,
        filters: InvestigationRequest,
    ):

        rows = await investigate_repository.get_event_timeline(
            filters
        )

        return TimelineResponse(
            points=[
                TimelinePoint(
                    timestamp=row["activity_date"],
                    success_count=row["success_count"],
                    failure_count=row["failure_count"],
                    exclusion_count=row["exclusion_count"],
                    appearance_count=row["total_events"],
                )
                for row in rows
            ]
        )

    # ==========================================================
    # EMPLOYEE OVERVIEW
    # ==========================================================

    async def get_employee_overview(
        self,
        employee_id: int,
    ):

        profile, devices = await asyncio.gather(
            investigate_repository.get_employee_profile(
                employee_id
            ),
            investigate_repository.get_employee_devices(
                employee_id
            ),
        )

        return {
            "profile": dict(profile) if profile else None,
            "devices": [
                dict(device)
                for device in devices
            ]
        }

    # ==========================================================
    # MAC DETAIL
    # ==========================================================

    async def get_mac_details(
        self,
        user_mac: str,
    ):

        row = await investigate_repository.get_mac_details(
            user_mac
        )

        if not row:
            return None

        return dict(row)

    # ==========================================================
    # FILTER OPTIONS
    # ==========================================================

    async def get_filter_options(
        self,
    ):

        (
            ssids,
            statuses,
            mnemonics,
            locations,
            facilities,
            aps,
        ) = await asyncio.gather(
            investigate_repository.get_ssid_options(),
            investigate_repository.get_status_options(),
            investigate_repository.get_mnemonic_options(),
            investigate_repository.get_location_options(),
            investigate_repository.get_facility_options(),
            investigate_repository.get_ap_options(),
        )

        return FilterOptionsResponse(
            ssids=[
                row["ssid"]
                for row in ssids
                if row["ssid"]
            ],
            statuses=[
                row["status"]
                for row in statuses
            ],
            mnemonics=[
                row["mnemonic"]
                for row in mnemonics
            ],
            locations=[
                row["location"]
                for row in locations
            ],
            facilities=[
                row["facility"]
                for row in facilities
            ],
            ap_hostnames=[
                row["ap_hostname"]
                for row in aps
            ],
        )

    # ==========================================================
    # GLOBAL SEARCH
    # ==========================================================

    async def global_search(
        self,
        query: str,
        page: int = 1,
        page_size: int = 20,
    ):

        (
            employees,
            macs,
            ssids,
            aps,
            locations,
        ) = await asyncio.gather(
            investigate_repository.search_employee(
                query
            ),
            investigate_repository.search_mac(
                query
            ),
            investigate_repository.search_ssid(
                query
            ),
            investigate_repository.search_ap(
                query
            ),
            investigate_repository.search_location(
                query
            ),
        )

        results = []

        results.extend(
            [
                SearchResult(
                    entity_type="Employee",
                    display_value=str(
                        row["employee_id"]
                    ),
                    matched_field="employee_id",
                )
                for row in employees
            ]
        )

        results.extend(
            [
                SearchResult(
                    entity_type="MAC",
                    display_value=row["user_mac"],
                    matched_field="user_mac",
                )
                for row in macs
            ]
        )

        results.extend(
            [
                SearchResult(
                    entity_type="SSID",
                    display_value=row["ssid"],
                    matched_field="ssid",
                )
                for row in ssids
            ]
        )

        results.extend(
            [
                SearchResult(
                    entity_type="AP",
                    display_value=row["ap_hostname"],
                    matched_field="ap_hostname",
                )
                for row in aps
            ]
        )

        results.extend(
            [
                SearchResult(
                    entity_type="Location",
                    display_value=row["location"],
                    matched_field="location",
                )
                for row in locations
            ]
        )

        total_records = len(results)

        return GlobalSearchResponse(
            results=results[
                0:
                min(
                    total_records,
                    page_size,
                )
            ],
            pagination=PaginationMeta(
                page=page,
                page_size=page_size,
                total_records=total_records,
                total_pages=math.ceil(
                    total_records / page_size
                ),
            ),
        )

    # ==========================================================
    # SEARCH SUMMARY
    # ==========================================================

    async def get_summary(
        self,
        filters: InvestigationRequest,
    ) -> InvestigationSummary:

        total_events = await investigate_repository.count_events(
            filters
        )

        return InvestigationSummary(
            total_devices=0,
            total_users=0,
            valid_users=0,
            invalid_users=0,
            success_rate=0,
            failure_rate=0,
            recovery_rate=0,
        )


investigate_service = InvestigateService()