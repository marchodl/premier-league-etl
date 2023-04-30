with max_ts AS (
    SELECT max(current_ts) AS max_ts FROM {{ ref('raw_yellow_cards') }} 
)


SELECT
    *,
    round(minutes_played / total_yellow_cards,2) AS yellow_card_per_minute_played
FROM {{ ref('raw_yellow_cards') }} 
WHERE current_ts >=  (SELECT * FROM max_ts)