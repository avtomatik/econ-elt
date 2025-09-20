from enum import Enum
from functools import cache
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

from .core.config import DATA_DIR


class Token(str, Enum):

    def __new__(cls, value, usecols):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.usecols = usecols
        return obj

    DOUGLAS = 'dataset_douglas.zip', range(4, 7)
    USA_BROWN = 'dataset_usa_brown.zip', range(5, 8)
    USA_COBB_DOUGLAS = 'dataset_usa_cobb-douglas.zip', range(5, 8)
    USA_KENDRICK = 'dataset_usa_kendrick.zip', range(4, 7)
    USA_MC_CONNELL = 'dataset_usa_mc_connell_brue.zip', range(1, 4)
    USCB = 'dataset_uscb.zip', range(9, 12)

    def get_kwargs(self) -> dict[str, Any]:

        NAMES = ['series_id', 'period', 'value']

        return {
            'filepath_or_buffer': DATA_DIR / self.value,
            'header': 0,
            'names': NAMES,
            'index_col': 1,
            'skiprows': (0, 4)[self.value == 'dataset_usa_brown.zip'],
            'usecols': self.usecols,
        }


def stockpile_usa_hist(series_ids: dict[str, Token]) -> pd.DataFrame:
    """
    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================
    """
    return pd.concat(
        map(
            lambda _: load_dataset(_[-1]).pipe(filter_series, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )


def calculate_power_function_fit_params_a(df: pd.DataFrame, params: tuple[float]) -> None:
    """
    Parameters
    ----------
    df : pd.DataFrame
    ================== =================================
    df.index           Regressor: = Period
    df.iloc[:, 0]      Regressand
    ================== =================================
    params : tuple[float]
        Parameters.
    Returns
    -------
    None.
    """
    df.reset_index(level=0, inplace=True)
    _t_0 = df.iloc[:, 0].min() - 1
    # =========================================================================
    # {RESULT}(Yhat) = params[0] + params[1]*(T-T_0)**params[2]
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(_t_0).pow(
        params[2]).mul(params[1]).add(params[0])
    print(f'Model Parameter: T_0 = {_t_0};')
    print(f'Model Parameter: Y_0 = {params[0]};')
    print(f'Model Parameter: A = {params[1]:.4f};')
    print(f'Model Parameter: Alpha = {params[2]:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 2].mean():,.4f};')
    print(
        f'Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};'
    )
    print(
        f'Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}.'
    )


def calculate_power_function_fit_params_b(df: pd.DataFrame, params: tuple[float]) -> None:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Regressor
        df.iloc[:, 1]      Regressand
        ================== =================================
    params : tuple[float]
        Model Parameters.
    Returns
    -------
    None.
    """
    _param = (params[3]-params[2])/(params[1]-params[0])**params[4]
    # =========================================================================
    # '{RESULT}(Yhat) = U_1 + ((U_2-U_1)/(TAU_2-TAU_1)**Alpha)*({X}-TAU_1)**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:, 0].sub(params[0]).pow(
        params[4]).mul(_param).add(params[2])
    print(f'Model Parameter: TAU_1 = {params[0]};')
    print(f'Model Parameter: TAU_2 = {params[1]};')
    print(f'Model Parameter: U_1 = {params[2]};')
    print(f'Model Parameter: U_2 = {params[3]};')
    print(f'Model Parameter: Alpha = {params[4]:.4f};')
    print(
        f'Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {_param:,.4f};'
    )
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print(
        f'Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};'
    )
    print(
        f'Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}.'
    )


def calculate_power_function_fit_params_c(df: pd.DataFrame, params: tuple[float]) -> None:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Regressor
        df.iloc[:, 1]      Regressand
        ================== =================================
    params : tuple[float]
        Model Parameters.
    Returns
    -------
    None.
    """
    _alpha = np.divide(
        np.subtract(*map(np.log, params[::-1][:2])),
        np.subtract(*map(np.log, params[:2]))
    )
    # =========================================================================
    # '{RESULT}{Hat}{Y} = Y_1*(X_1/{X})**Alpha'
    # =========================================================================
    df[f'estimate_{df.columns[-1]}'] = df.iloc[:,
                                               0].rdiv(params[0]).pow(_alpha).mul(params[2])
    print(f'Model Parameter: X_1 = {params[0]:.4f};')
    print(f'Model Parameter: X_2 = {params[1]};')
    print(f'Model Parameter: Y_1 = {params[2]:.4f};')
    print(f'Model Parameter: Y_2 = {params[3]};')
    print(f'Model Parameter: Alpha: = LN(Y_2/Y_1)/LN(X_1/X_2) = {_alpha:.4f};')
    print(f'Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};')
    print(
        f'Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};'
    )
    print(
        f'Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}.'
    )


@cache
def load_dataset(token: Token) -> pd.DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    token : Token

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """
    return pd.read_csv(**token.get_kwargs())


def filter_series(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={'value': series_id}
    )


MAP_MC_CONNEL = {
    'Ставка прайм-рейт, %': 'prime_rate',
    'Валовой объем внутренних частных инвестиций, млрд долл. США': 'A006RC',
    'Национальный доход, млрд долл. США': 'A032RC',
    'Валовой внутренний продукт, млрд долл. США': 'A191RC',
}


def main(year_base: int = 1980) -> None:
    """
    Power Function Approximation

    Returns
    -------
    None
        DESCRIPTION.
    """

    SERIES_IDS = {
        'Валовой внутренний продукт, млрд долл. США': Token.USA_MC_CONNELL
    }
    PARAMS = (2800, 0.01, 0.5)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_a, PARAMS
    )

    SERIES_IDS = {
        'Ставка прайм-рейт, %': Token.USA_MC_CONNELL,
        'Национальный доход, млрд долл. США': Token.USA_MC_CONNELL,
    }
    PARAMS = (4, 12, 9000, 3000, 0.87)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_b, PARAMS
    )

    SERIES_IDS = {
        'Ставка прайм-рейт, %': Token.USA_MC_CONNELL,
        'Валовой объем внутренних частных инвестиций, млрд долл. США': Token.USA_MC_CONNELL,
    }
    PARAMS = (1.5, 19, 1.7, 1760)
    stockpile_usa_hist(SERIES_IDS).truncate(before=year_base).rename(columns=MAP_MC_CONNEL).pipe(
        calculate_power_function_fit_params_c, PARAMS
    )


if __name__ == '__main__':
    main()
