SELECT
s.*
FROM  {{ ref('staging_ranking') }}  r
INNER JOIN {{ ref('stadiums_with_GPS_coordinates') }} s 
    ON TRIM(r.name) = TRIM(s.team)