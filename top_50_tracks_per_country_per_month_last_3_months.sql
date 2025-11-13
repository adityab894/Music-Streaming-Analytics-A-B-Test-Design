WITH central_europe AS (
  SELECT country
  FROM UNNEST([
    'AT','HR','CZ','DE','HU','LT','PL','SK','SI','CH','LI'
  ]) AS country
),
monthly_track_durations AS (
  SELECT 
    p.track_id,
    tr.artist,
    u.country,
    FORMAT_DATE('%Y-%m', p.play_date) AS year_month,
    SUM(p.play_duration_seconds) AS total_play_duration
  FROM `central_europe_plays.plays` p
  LEFT JOIN `central_europe_plays.user` u ON p.user_id = u.id 
  LEFT JOIN `central_europe_plays.tracks` tr ON p.track_id = tr.Id
  WHERE DATE(p.play_date) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND CURRENT_DATE()
    AND u.country IN (SELECT country FROM central_europe)
  GROUP BY p.track_id, tr.artist, u.country, year_month
),
ranked_tracks AS (
  SELECT 
    *,
    DENSE_RANK() OVER (
      PARTITION BY country, year_month 
      ORDER BY total_play_duration DESC, track_id ASC
    ) AS track_rank
  FROM monthly_track_durations
)
SELECT
  track_id,
  artist,
  country,
  year_month,
  total_play_duration,
  track_rank
FROM ranked_tracks
WHERE track_rank <= 50
ORDER BY country, year_month DESC, total_play_duration DESC;