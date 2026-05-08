from approx.funcs import (bounded_power_interpolation, inverse_power_scaling,
                          offset_power_growth)
from core.warehouse import stockpile_usa_hist


def main(year_base: int = 1980) -> None:
    """
    Power Function Approximation

    Returns
    -------
    None
        DESCRIPTION.
    """
    relation = stockpile_usa_hist(["A191RC"])

    relation = relation.filter(f"period >= {year_base}")

    relation = offset_power_growth(
        relation,
        period_col="period",
        value_col="A191RC",
        y0=2800,
        a=0.01,
        alpha=0.5,
    )

    print(
        relation.aggregate(
            """
            AVG(A191RC) AS mean_actual,
            AVG(squared_error) AS msd,
            SQRT(AVG(squared_error)) AS rmsd
        """
        ).fetchall()
    )

    relation = stockpile_usa_hist(["prime_rate", "A032RC"])

    relation = relation.filter(f"period >= {year_base}")

    relation = bounded_power_interpolation(
        relation,
        x_col="prime_rate",
        y_col="A032RC",
        tau1=4,
        tau2=12,
        u1=9000,
        u2=3000,
        alpha=0.87,
    )

    print(
        relation.aggregate(
            """
            AVG(A032RC) AS mean_actual,
            AVG(squared_error) AS msd,
            SQRT(AVG(squared_error)) AS rmsd
            """
        ).fetchall()
    )

    relation = stockpile_usa_hist(["prime_rate", "A006RC"])

    relation = relation.filter(f"period >= {year_base}")

    relation = inverse_power_scaling(
        relation,
        x_col="prime_rate",
        y_col="A006RC",
        x1=1.5,
        x2=19,
        y1=1.7,
        y2=1760,
    )

    print(
        relation.aggregate(
            """
            AVG(A006RC) AS mean_actual,
            AVG(squared_error) AS msd,
            SQRT(AVG(squared_error)) AS rmsd
            """
        ).fetchall()
    )


if __name__ == "__main__":
    main()
