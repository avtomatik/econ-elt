WITH inv AS (
    SELECT period, value AS investment
    FROM {{ ref('stg_series') }}
    WHERE series_id = 'investment'
),

rate AS (
    SELECT period, value AS prime_rate
    FROM {{ ref('stg_series') }}
    WHERE series_id = 'prime_rate'
),

base AS (
    SELECT *
    FROM inv
    LEFT JOIN rate USING (period)
    WHERE period >= 1980
),

model AS (
    SELECT
        *,
        (
            1.7 * POWER(1.5 / prime_rate, LOG(1760 / 1.7) / LOG(1.5 / 19))
        ) AS estimate
    FROM base
)

SELECT
    *,
    POWER(investment - estimate, 2) AS squared_error
FROM model
