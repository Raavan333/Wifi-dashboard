# ============================================================
# RECOVERY ANALYSIS
# ============================================================

RECOVERY_ANALYSIS_QUERY = """
WITH user_status AS (
    SELECT
        user_mac,

        BOOL_OR(status = 'FAIL')
            AS had_failure,

        BOOL_OR(status = 'SUCCESS')
            AS had_success

    FROM wifi_event_history

    GROUP BY user_mac
)

SELECT

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
)
AS failed_users,

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
    AND had_success = TRUE
)
AS recovered_users,

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
    AND had_success = FALSE
)
AS unrecovered_users

FROM user_status;
"""


# ============================================================
# RECOVERY ANALYSIS VALID USERS ONLY
# ============================================================

RECOVERY_ANALYSIS_VALID_USERS_QUERY = """
WITH valid_users AS (

    SELECT user_mac

    FROM wifi_user_summary

    WHERE employee_id IS NOT NULL
      AND ux_available = TRUE
      AND total_success_count > 0
),

user_status AS (

    SELECT
        weh.user_mac,

        BOOL_OR(weh.status = 'FAIL')
            AS had_failure,

        BOOL_OR(weh.status = 'SUCCESS')
            AS had_success

    FROM wifi_event_history weh

    INNER JOIN valid_users vu
        ON vu.user_mac = weh.user_mac

    GROUP BY weh.user_mac
)

SELECT

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
)
AS failed_users,

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
    AND had_success = TRUE
)
AS recovered_users,

COUNT(*)
FILTER (
    WHERE had_failure = TRUE
    AND had_success = FALSE
)
AS unrecovered_users

FROM user_status;
"""


# ============================================================
# CONNECTION OUTCOME DISTRIBUTION
# ============================================================

OUTCOME_DISTRIBUTION_QUERY = """
SELECT

COUNT(*)
FILTER (
    WHERE total_success_count > 0
    AND total_failure_count = 0
)
AS success_only,

COUNT(*)
FILTER (
    WHERE total_success_count > 0
    AND total_failure_count > 0
)
AS success_and_failure,

COUNT(*)
FILTER (
    WHERE total_success_count = 0
    AND total_failure_count > 0
)
AS failure_only,

COUNT(*)
FILTER (
    WHERE total_exclusion_count > 0
)
AS exclusion_devices

FROM wifi_user_summary;
"""


# ============================================================
# TOP FAILURE SSIDS
# ============================================================

TOP_FAILURE_SSIDS_QUERY = """
SELECT
    ssid,

    COUNT(*) AS failure_count

FROM wifi_event_history

WHERE status = 'FAILURE'
AND ssid IS NOT NULL

GROUP BY ssid

ORDER BY failure_count DESC

LIMIT $1;
"""


# ============================================================
# TOP INVALID SSIDS
# ============================================================

TOP_INVALID_SSIDS_QUERY = """
SELECT
    unnest(observed_ssids) AS ssid,

    COUNT(*) AS invalid_count

FROM wifi_user_summary

WHERE total_success_count = 0

GROUP BY ssid

ORDER BY invalid_count DESC

LIMIT $1;
"""


# ============================================================
# AP FAILURE ANALYSIS
# ============================================================

TOP_FAILURE_APS_QUERY = """
SELECT
    ap_hostname,

    COUNT(*) AS affected_devices,

    SUM(total_failure_count) AS failure_count

FROM wifi_user_summary

WHERE ap_hostname IS NOT NULL
AND ap_hostname <> 'NA'

GROUP BY ap_hostname

ORDER BY failure_count DESC

LIMIT $1;
"""


# ============================================================
# SSID UTILIZATION
# ============================================================

SSID_UTILIZATION_QUERY = """
SELECT
    ssid,

    COUNT(DISTINCT user_mac) AS users

FROM (

    SELECT
        user_mac,
        unnest(observed_ssids) AS ssid

    FROM wifi_user_summary

) x

GROUP BY ssid

ORDER BY users DESC;
"""


# ============================================================
# LOCATION SUCCESS RATES
# ============================================================

LOCATION_SUCCESS_RATES_QUERY = """
SELECT

location,

SUM(total_success_count)
AS successes,

SUM(total_failure_count)
AS failures,

ROUND(
100.0 *
SUM(total_success_count)
/
NULLIF(
SUM(total_success_count)
+
SUM(total_failure_count)
,0
)
,2
)
AS success_rate

FROM wifi_user_summary

WHERE location IS NOT NULL
AND location <> 'NA'

GROUP BY location

ORDER BY success_rate DESC;
"""


# ============================================================
# NEW USERS DAILY
# ============================================================

NEW_USERS_DAILY_QUERY = """
SELECT

DATE(first_seen_timestamp)
AS activity_date,

COUNT(*)
AS user_count

FROM wifi_user_summary

WHERE first_seen_timestamp IS NOT NULL

GROUP BY DATE(first_seen_timestamp)

ORDER BY activity_date;
"""


# ============================================================
# ACTIVE USERS DAILY
# ============================================================

ACTIVE_USERS_DAILY_QUERY = """
SELECT

DATE(last_seen_timestamp)
AS activity_date,

COUNT(*)
AS user_count

FROM wifi_user_summary

WHERE last_seen_timestamp IS NOT NULL

GROUP BY DATE(last_seen_timestamp)

ORDER BY activity_date;
"""


# ============================================================
# EVENT TIMELINE
# ============================================================

EVENT_TIMELINE_QUERY = """
SELECT

DATE(appeared_timestamp)
AS activity_date,

COUNT(*)
FILTER (
    WHERE status = 'SUCCESS'
)
AS success_events,

COUNT(*)
FILTER (
    WHERE status = 'FAIL'
)
AS failure_events,

COUNT(*)
FILTER (
    WHERE status = 'EXCLUSION'
)
AS exclusion_events

FROM wifi_event_history

GROUP BY DATE(appeared_timestamp)

ORDER BY activity_date;
"""