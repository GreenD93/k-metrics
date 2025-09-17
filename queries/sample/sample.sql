-- params:
--   start_date, end_date, limit(optional)

SELECT
  channel,
  COUNT(*) AS event_count
FROM prod.raw.app_events
WHERE date(event_ts) BETWEEN date('{{ start_date }}') AND date('{{ end_date }}')
GROUP BY channel
ORDER BY event_count DESC
LIMIT {{ limit }};