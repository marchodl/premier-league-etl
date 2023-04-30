SELECT
*
FROM {{ ref('staging_ranking') }} 
WHERE PLAYED > 38