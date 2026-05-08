import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


def calculate_power_function_fit_params_a(
    df: pd.DataFrame, params: tuple[float, float, float]
) -> None:
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
    df[f"estimate_{df.columns[-1]}"] = (
        df.iloc[:, 0].sub(_t_0).pow(params[2]).mul(params[1]).add(params[0])
    )
    print(f"Model Parameter: T_0 = {_t_0};")
    print(f"Model Parameter: Y_0 = {params[0]};")
    print(f"Model Parameter: A = {params[1]:.4f};")
    print(f"Model Parameter: Alpha = {params[2]:.4f};")
    print(f"Estimator Result: Mean Value: {df.iloc[:, 2].mean():,.4f};")
    print(
        f"Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};"
    )
    print(
        f"Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}."
    )


def calculate_power_function_fit_params_b(
    df: pd.DataFrame, params: tuple[float, float, float, float, float]
) -> None:
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
    _param = (params[3] - params[2]) / (params[1] - params[0]) ** params[4]
    # =========================================================================
    # '{RESULT}(Yhat) = U_1 + ((U_2-U_1)/(TAU_2-TAU_1)**Alpha)*({X}-TAU_1)**Alpha'
    # =========================================================================
    df[f"estimate_{df.columns[-1]}"] = (
        df.iloc[:, 0].sub(params[0]).pow(params[4]).mul(_param).add(params[2])
    )
    print(f"Model Parameter: TAU_1 = {params[0]};")
    print(f"Model Parameter: TAU_2 = {params[1]};")
    print(f"Model Parameter: U_1 = {params[2]};")
    print(f"Model Parameter: U_2 = {params[3]};")
    print(f"Model Parameter: Alpha = {params[4]:.4f};")
    print(
        f"Model Parameter: A: = (U_2-U_1)/(TAU_2-TAU_1)**Alpha = {_param:,.4f};"
    )
    print(f"Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};")
    print(
        f"Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};"
    )
    print(
        f"Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}."
    )


def calculate_power_function_fit_params_c(
    df: pd.DataFrame, params: tuple[float, float, float, float]
) -> None:
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
        np.subtract(*map(np.log, params[:2])),
    )
    # =========================================================================
    # '{RESULT}{Hat}{Y} = Y_1*(X_1/{X})**Alpha'
    # =========================================================================
    df[f"estimate_{df.columns[-1]}"] = (
        df.iloc[:, 0].rdiv(params[0]).pow(_alpha).mul(params[2])
    )
    print(f"Model Parameter: X_1 = {params[0]:.4f};")
    print(f"Model Parameter: X_2 = {params[1]};")
    print(f"Model Parameter: Y_1 = {params[2]:.4f};")
    print(f"Model Parameter: Y_2 = {params[3]};")
    print(f"Model Parameter: Alpha: = LN(Y_2/Y_1)/LN(X_1/X_2) = {_alpha:.4f};")
    print(f"Estimator Result: Mean Value: {df.iloc[:, 1].mean():,.4f};")
    print(
        f"Estimator Result: Mean Squared Deviation, MSD: {mean_squared_error(df.iloc[:, 1], df.iloc[:, 2]):,.4f};"
    )
    print(
        f"Estimator Result: Root-Mean-Square Deviation, RMSD: {np.sqrt(mean_squared_error(df.iloc[:, 1], df.iloc[:, 2])):,.4f}."
    )
