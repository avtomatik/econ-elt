from calcs.funcs import (calculate_power_function_fit_params_a,
                         calculate_power_function_fit_params_b,
                         calculate_power_function_fit_params_c)
from core.backend import stockpile_usa_hist


def main(year_base: int = 1980) -> None:
    """
    Power Function Approximation

    Returns
    -------
    None
        DESCRIPTION.
    """

    SERIES_IDS = ["A191RC"]
    PARAMS = (2800, 0.01, 0.5)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).pipe(
        calculate_power_function_fit_params_a, PARAMS
    )

    SERIES_IDS = ["prime_rate", "A032RC"]
    PARAMS = (4, 12, 9000, 3000, 0.87)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).pipe(
        calculate_power_function_fit_params_b, PARAMS
    )

    SERIES_IDS = ["prime_rate", "A006RC"]
    PARAMS = (1.5, 19, 1.7, 1760)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).pipe(
        calculate_power_function_fit_params_c, PARAMS
    )


if __name__ == "__main__":
    main()
