import math


def offset_power_growth(
    relation,
    *,
    period_col: str,
    value_col: str,
    y0: float,
    a: float,
    alpha: float,
) -> None:

    query = f"""
        WITH model AS (
            SELECT
                *,
                MIN({period_col}) OVER () - 1 AS t0,
                (
                    {y0}
                    + {a}
                    * POWER(
                        {period_col}
                        - (MIN({period_col}) OVER () - 1),
                        {alpha}
                    )
                ) AS estimate
            FROM relation
        )

        SELECT
            *,
            POWER({value_col} - estimate, 2) AS squared_error
        FROM model
    """

    return relation.query("relation", query)


def bounded_power_interpolation(
    relation,
    *,
    x_col: str,
    y_col: str,
    tau1: float,
    tau2: float,
    u1: float,
    u2: float,
    alpha: float,
) -> None:
    a = (u2 - u1) / ((tau2 - tau1) ** alpha)
    query = f"""
        WITH model AS (
            SELECT
                *,
                (
                    {u1}
                    + (
                        {a}
                        * POWER(
                            {x_col} - {tau1},
                            {alpha}
                        )
                    )
                ) AS estimate
            FROM relation
        )

        SELECT
            *,
            POWER(
                {y_col} - estimate,
                2
            ) AS squared_error
        FROM model
    """

    return relation.query("relation", query)


def inverse_power_scaling(
    relation,
    *,
    x_col: str,
    y_col: str,
    x1: float,
    x2: float,
    y1: float,
    y2: float,
) -> None:
    alpha = math.log(y2 / y1) / math.log(x1 / x2)

    query = f"""
        WITH model AS (
            SELECT
                *,
                (
                    {y1}
                    * POWER(
                        {x1} / {x_col},
                        {alpha}
                    )
                ) AS estimate
            FROM relation
        )

        SELECT
            *,
            POWER(
                {y_col} - estimate,
                2
            ) AS squared_error
        FROM model
    """

    return relation.query("relation", query)
