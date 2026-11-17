# ============================================================
# BASE EVENT QUERY
# ============================================================

BASE_EVENTS_QUERY = """
SELECT

    weh.id,

    weh.user_mac,

    wus.employee_id,

    weh.facility,

    weh.mnemonic,

    weh.status,

    weh.ssid,

    weh.appeared_timestamp,

    weh.elasticsearch_timestamp,

    wus.location,

    wus.ap_hostname

FROM wifi_event_history weh

LEFT JOIN wifi_user_summary wus
ON weh.user_mac = wus.user_mac
"""


# ============================================================
# EVENT COUNT
# ============================================================

BASE_EVENTS_COUNT_QUERY = """
SELECT COUNT(*)

FROM wifi_event_history weh

LEFT JOIN wifi_user_summary wus
ON weh.user_mac = wus.user_mac
"""


# ============================================================
# USER DEVICE LOOKUP
# ============================================================

USER_DEVICES_QUERY = """
SELECT

    user_mac,

    employee_id,

    total_appearance_count,

    total_success_count,

    total_failure_count,

    total_exclusion_count,

    first_seen_timestamp,

    last_seen_timestamp,

    observed_duration,

    ux_available,

    location,

    ap_hostname,

    observed_ssids

FROM wifi_user_summary
"""


# ============================================================
# EMPLOYEE PROFILE
# ============================================================

EMPLOYEE_PROFILE_QUERY = """
SELECT

    employee_id,

    COUNT(*) AS total_devices,

    SUM(total_success_count)
        AS total_success_count,

    SUM(total_failure_count)
        AS total_failure_count,

    MIN(first_seen_timestamp)
        AS first_seen_timestamp,

    MAX(last_seen_timestamp)
        AS last_seen_timestamp

FROM wifi_user_summary
"""


# ============================================================
# TIMELINE
# ============================================================

EVENT_TIMELINE_QUERY = """
SELECT

    DATE(appeared_timestamp)
        AS activity_date,

    COUNT(*)
    FILTER (
        WHERE status = 'SUCCESS'
    )
    AS success_count,

    COUNT(*)
    FILTER (
        WHERE status = 'FAIL'
    )
    AS failure_count,

    COUNT(*)
    FILTER (
        WHERE status = 'EXCLUSION'
    )
    AS exclusion_count,

    COUNT(*)
    AS total_events

FROM wifi_event_history
"""


# ============================================================
# STATUS DISTRIBUTION
# ============================================================

STATUS_DISTRIBUTION_QUERY = """
SELECT

    status,

    COUNT(*) AS event_count

FROM wifi_event_history
"""


# ============================================================
# MNEMONIC DISTRIBUTION
# ============================================================

MNEMONIC_DISTRIBUTION_QUERY = """
SELECT

    mnemonic,

    COUNT(*) AS event_count

FROM wifi_event_history
"""


# ============================================================
# GLOBAL SEARCH - EMPLOYEE
# ============================================================

SEARCH_EMPLOYEE_QUERY = """
SELECT DISTINCT
    employee_id
FROM wifi_user_summary
WHERE employee_id IS NOT NULL
"""


# ============================================================
# GLOBAL SEARCH - MAC
# ============================================================
SEARCH_MAC_QUERY = """
SELECT
    user_mac
FROM wifi_user_summary
"""


# ============================================================
# GLOBAL SEARCH - SSID
# ============================================================

SEARCH_SSID_QUERY = """
SELECT DISTINCT
    ssid
FROM (
    SELECT
        UNNEST(observed_ssids) AS ssid
    FROM wifi_user_summary
) t
"""

# ============================================================
# GLOBAL SEARCH - AP
# ============================================================

SEARCH_AP_QUERY = """
SELECT DISTINCT
    ap_hostname
FROM wifi_user_summary
WHERE ap_hostname IS NOT NULL
AND ap_hostname <> 'NA'
"""


# ============================================================
# GLOBAL SEARCH - LOCATION
# ============================================================

SEARCH_LOCATION_QUERY = """
SELECT DISTINCT
    location
FROM wifi_user_summary
WHERE location IS NOT NULL
AND location <> 'NA'
"""



# ============================================================
# FILTER OPTIONS
# ============================================================

FILTER_SSIDS_QUERY = """
SELECT DISTINCT

    UNNEST(observed_ssids)
    AS ssid

FROM wifi_user_summary

ORDER BY 1;
"""


FILTER_STATUSES_QUERY = """
SELECT DISTINCT

    status

FROM wifi_event_history

ORDER BY status;
"""


FILTER_MNEMONICS_QUERY = """
SELECT DISTINCT

    mnemonic

FROM wifi_event_history

ORDER BY mnemonic;
"""


FILTER_LOCATIONS_QUERY = """
SELECT DISTINCT

    location

FROM wifi_user_summary

WHERE location IS NOT NULL
AND location <> 'NA'

ORDER BY location;
"""


FILTER_FACILITIES_QUERY = """
SELECT DISTINCT

    facility

FROM wifi_event_history

ORDER BY facility;
"""


FILTER_APS_QUERY = """
SELECT DISTINCT

    ap_hostname

FROM wifi_user_summary

WHERE ap_hostname IS NOT NULL
AND ap_hostname <> 'NA'

ORDER BY ap_hostname;
"""