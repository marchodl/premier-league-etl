SELECT *
FROM {{ source('premier_league', 'yellow_cards') }}
