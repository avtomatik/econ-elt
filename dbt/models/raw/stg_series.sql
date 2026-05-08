SELECT
    period,

    CASE
        WHEN series_id = 'Ставка прайм-рейт, %'
            THEN 'prime_rate'

        WHEN series_id = 'Валовой внутренний продукт, млрд долл. США'
            THEN 'gdp'

        WHEN series_id = 'Национальный доход, млрд долл. США'
            THEN 'income'

        WHEN series_id = 'Валовой объем внутренних частных инвестиций, млрд долл. США'
            THEN 'investment'

        ELSE NULL
    END AS series_id,

    value

FROM raw.mc_connell_brue
