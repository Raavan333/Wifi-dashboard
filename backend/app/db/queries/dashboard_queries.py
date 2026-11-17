# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

EXECUTIVE_SUMMARY_QUERY = """
SELECT
    COUNT(*) AS total_devices,

    COUNT(DISTINCT employee_id)
        FILTER (
            WHERE employee_id IS NOT NULL
        ) AS total_users,

    COUNT(*)
        FILTER (
            WHERE employee_id IS NOT NULL
            AND total_success_count > 0
            AND ux_available = TRUE
        ) AS valid_users,

    COUNT(*)
        FILTER (
            WHERE total_success_count = 0
        ) AS invalid_devices,

    COUNT(*)
        FILTER (
            WHERE total_success_count > 0
            AND ux_available = FALSE
        ) AS ux_unavailable_users

FROM wifi_user_summary;
"""


# ============================================================
# SUCCESS / FAILURE
# ============================================================

SUCCESS_FAILURE_QUERY = """
SELECT
    SUM(total_success_count) AS success_count,
    SUM(total_failure_count) AS failure_count
FROM wifi_user_summary;
"""


# ============================================================
# USER POPULATION
# ============================================================

USER_POPULATION_QUERY = """
SELECT
    COUNT(*)
        FILTER (
            WHERE employee_id IS NOT NULL
            AND total_success_count > 0
            AND ux_available = TRUE
        ) AS valid_users,

    COUNT(DISTINCT employee_id)
        FILTER (
            WHERE employee_id IS NOT NULL
            AND (
                SELECT COUNT(*)
                FROM wifi_user_summary w2
                WHERE w2.employee_id =
                      wifi_user_summary.employee_id
            ) > 1
        ) AS multi_device_users
FROM wifi_user_summary;
"""


# ============================================================
# DEVICE DISTRIBUTION
# ============================================================

DEVICE_DISTRIBUTION_QUERY = """
WITH device_counts AS (
    SELECT
        employee_id,
        COUNT(*) AS device_count
    FROM wifi_user_summary
    WHERE employee_id IS NOT NULL
    GROUP BY employee_id
)

SELECT
    CASE
        WHEN device_count = 1 THEN '1 Device'
        WHEN device_count = 2 THEN '2 Devices'
        WHEN device_count = 3 THEN '3 Devices'
        WHEN device_count BETWEEN 4 AND 5
            THEN '4-5 Devices'
        ELSE '6+ Devices'
    END AS bucket,

    COUNT(*) AS user_count

FROM device_counts

GROUP BY bucket

ORDER BY bucket;
"""


# ============================================================
# RECENT MAC COUNTS
# ============================================================

RECENT_ACTIVITY_QUERY = """
SELECT

COUNT(*)
FILTER (
    WHERE last_seen_timestamp >=
          NOW() - INTERVAL '7 days'
)
AS macs_last_7_days,

COUNT(*)
FILTER (
    WHERE last_seen_timestamp >=
          NOW() - INTERVAL '30 days'
)
AS macs_last_30_days,

COUNT(*)
FILTER (
    WHERE last_seen_timestamp >=
          NOW() - INTERVAL '90 days'
)
AS macs_last_90_days

FROM wifi_user_summary;
"""


# ============================================================
# CONNECTIVITY HEALTH
# ============================================================

CONNECTIVITY_HEALTH_QUERY = """
SELECT

SUM(total_success_count)
AS total_success,

SUM(total_failure_count)
AS total_failure,

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
AS success_rate,

ROUND(
100.0 *
SUM(total_failure_count)
/
NULLIF(
SUM(total_success_count)
+
SUM(total_failure_count)
,0
)
,2
)
AS failure_rate

FROM wifi_user_summary;
"""


# ============================================================
# SSID USER DISTRIBUTION
# ============================================================

SSID_DISTRIBUTION_QUERY = """
SELECT
    ssid,
    COUNT(DISTINCT user_mac) AS user_count

FROM (
    SELECT
        user_mac,
        UNNEST(observed_ssids) AS ssid
    FROM wifi_user_summary
) tmp

GROUP BY ssid

ORDER BY user_count DESC

LIMIT $1;
"""


# ============================================================
# SSID COMBINATIONS
# ============================================================

SSID_COMBINATIONS_QUERY = """
SELECT
    ARRAY_TO_STRING(
        observed_ssids,
        ' + '
    ) AS ssid_combination,

    COUNT(*)
AS user_count

FROM wifi_user_summary

WHERE observed_ssids IS NOT NULL

GROUP BY observed_ssids

ORDER BY user_count DESC

LIMIT $1;
"""


# ============================================================
# LOCATION DISTRIBUTION
# ============================================================

LOCATION_DISTRIBUTION_QUERY = """
SELECT
    location,
    COUNT(*) AS device_count

FROM wifi_user_summary

WHERE location IS NOT NULL
AND location <> 'NA'

GROUP BY location

ORDER BY device_count DESC

LIMIT $1;
"""


# ============================================================
# OBSERVED DURATION DISTRIBUTION
# ============================================================

DURATION_DISTRIBUTION_QUERY = """
SELECT

CASE

WHEN observed_duration <
INTERVAL '1 day'
THEN '<1 Day'

WHEN observed_duration <
INTERVAL '7 days'
THEN '1-7 Days'

WHEN observed_duration <
INTERVAL '30 days'
THEN '7-30 Days'

WHEN observed_duration <
INTERVAL '60 days'
THEN '30-60 Days'

ELSE '60-90 Days'

END AS duration_bucket,

COUNT(*) AS user_count

FROM wifi_user_summary

GROUP BY duration_bucket;
"""


# ============================================================
# NEW USERS TREND
# ============================================================

NEW_USERS_TREND_QUERY = """
SELECT

DATE(first_seen_timestamp)
AS observation_date,

COUNT(*)
AS users

FROM wifi_user_summary

WHERE first_seen_timestamp IS NOT NULL

GROUP BY observation_date

ORDER BY observation_date;
"""


# ============================================================
# ACTIVE USERS TREND
# ============================================================

ACTIVE_USERS_TREND_QUERY = """
SELECT

DATE(last_seen_timestamp)
AS observation_date,

COUNT(*)
AS users

FROM wifi_user_summary

WHERE last_seen_timestamp IS NOT NULL

GROUP BY observation_date

ORDER BY observation_date;
"""


# ============================================================
# DATA QUALITY
# ============================================================

DATA_QUALITY_QUERY = """
SELECT

COUNT(*)
FILTER (
    WHERE employee_id IS NOT NULL
    AND total_success_count > 0
    AND ux_available = TRUE
)
AS valid_users,

COUNT(*)
FILTER (
    WHERE employee_id IS NULL
)
AS unmapped_users,

COUNT(*)
FILTER (
    WHERE total_success_count > 0
    AND ux_available = FALSE
)
AS ux_missing_users,

COUNT(*)
FILTER (
    WHERE total_success_count = 0
)
AS invalid_devices

FROM wifi_user_summary;
"""