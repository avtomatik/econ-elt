WITH income AS (
    SELECT period, value AS income
    FROM {{ ref('stg_series') }}
    WHERE series_id = 'income'
),

rate AS (
    SELECT period, value AS prime_rate
    FROM {{ ref('stg_series') }}
    WHERE series_id = 'prime_rate'
),

base AS (
    SELECT *
    FROM income
    LEFT JOIN rate USING (period)
    WHERE period >= 1980
),

model AS (
    SELECT
        *,
        (
            9000
            + ((3000 - 9000) / POWER((12 - 4), 0.87))
            * POWER(prime_rate - 4, 0.87)
        ) AS estimate
    FROM base
)

SELECT
    *,
    POWER(income - estimate, 2) AS squared_error
FROM model
