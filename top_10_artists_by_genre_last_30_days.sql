--TOP 10 artists grouped by Genre for the last 30 days.
-- Ambiguity| Do we want a single top 10 list per genre covering the entire 30 daz period., or do we want a separate top 10 list for each daz withint those 30 dazs&

-- Total rows| 2*30*10 or 2*10

WITH
daily_track_durations AS (
SELECT
  t.genre,
  t.artist,
  p.play_date,
  SUM(p.play_duration_seconds) AS total_play_duration,
FROM
  `central_europe_plays.plays2` p -- contains plays per date on track id
JOIN
  `central_europe_plays.tracks` t --contains artist name on track id
ON
  p.track_id = t.Id
WHERE
  DATE(p.play_date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY
  1,2,3

),


ranked_tracks AS (
  SELECT 
    *,
    -- Why dense rank
    DENSE_RANK() OVER (
      PARTITION BY genre,play_date 
      ORDER BY total_play_duration DESC, artist ASC
    ) AS artist_rank
  FROM daily_track_durations
)

SELECT
  play_date,
  genre,
  artist,
  total_play_duration,
  artist_rank
FROM ranked_tracks
WHERE 
  -- top 10 artist
  artist_rank <= 10
ORDER BY play_date , genre, artist_rank ASC