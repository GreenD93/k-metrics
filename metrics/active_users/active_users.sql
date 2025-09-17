-- params:
--   as_of_date: "YYYY-MM-DD"
--   time_grain: "day" | "week" | "month"
--   channel: optional

{% set g = time_grain %}
WITH src AS (
  SELECT
    user_id,
    event_ts,
    date(event_ts) AS d,
    channel, device, region
  FROM prod.raw.app_events
  WHERE date_trunc('{{ g }}', event_ts)
        = date_trunc('{{ g }}', from_iso8601_timestamp('{{ as_of_date }}'))
    {% if channel %} AND channel = {{ channel | sql_str }} {% endif %}
)
SELECT
  date(date_trunc('{{ g }}', event_ts)) AS period,  -- 주/월 시작일 등
  COUNT(DISTINCT user_id) AS active_users
FROM src
GROUP BY 1
ORDER BY 1;