WITH base AS (
    SELECT *
    FROM {{ ref('stg_series') }}
    WHERE series_id = 'gdp'
      AND period >= 1980
),

model AS (
    SELECT
        *,
        (2800 + 0.01 * POWER(period - MIN(period) OVER () + 1, 0.5)) AS estimate
    FROM base
)

SELECT
    *,
    POWER(value - estimate, 2) AS squared_error
FROM model
