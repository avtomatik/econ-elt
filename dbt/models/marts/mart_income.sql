SELECT
    AVG(income) AS mean_actual,
    AVG(squared_error) AS msd,
    SQRT(AVG(squared_error)) AS rmsd
FROM {{ ref('model_income') }}
