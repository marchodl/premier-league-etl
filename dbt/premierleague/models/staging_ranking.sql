with max_ts AS (
    SELECT max(current_ts) as max_ts FROM {{ ref('raw_ranking') }} 
)

SELECT
    *
FROM {{ ref('raw_ranking') }} 
WHERE current_ts >=  (SELECT * FROM max_ts)