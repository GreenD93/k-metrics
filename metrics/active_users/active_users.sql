-- params:
--   as_of_date: "YYYY-MM-DD"
--   time_grain: "day"|"week"|"month"
--   channel: optional

{% set WHERE_BY_GRAIN = {
  'day':   "date(event_ts) = date('{{ as_of_date }}')",
  'week':  "date_trunc('week',  event_ts) = date_trunc('week',  from_iso8601_timestamp('{{ as_of_date }}'))",
  'month': "date_trunc('month', event_ts) = date_trunc('month', from_iso8601_timestamp('{{ as_of_date }}'))"
} %}

WITH src AS (
  SELECT
    user_id,
    event_ts,
    date(event_ts) AS d,
    channel, device, region
  FROM prod.raw.app_events
  WHERE {{ WHERE_BY_GRAIN[time_grain] }}
    {% if channel %} AND channel = {{ channel | sql_str }} {% endif %}
)
SELECT
  date(date_trunc('{{ time_grain }}', event_ts)) AS period,
  COUNT(DISTINCT user_id) AS active_users
FROM src
GROUP BY 1
ORDER BY 1;