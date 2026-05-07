import pandas as pd

from ingest.core.constants import MAP_MC_CONNEL
from ingest.core.paths import DATA_DIR, FILE_NAME


def pull_by_series_id(df: pd.DataFrame, series_id: str) -> pd.DataFrame:
    return df[df["series_id"] == series_id][["value"]].rename(
        columns={"value": series_id}
    )


def stockpile_usa_hist(series_ids: list[str]) -> pd.DataFrame:
    df = pd.read_parquet(DATA_DIR / FILE_NAME).set_index("period")
    df["series_id"] = df["series_id"].map(MAP_MC_CONNEL)
    return pd.concat(
        [pull_by_series_id(df, s) for s in series_ids], axis=1
    ).sort_index()
