from pathlib import Path

import pandas as pd

from core.constants import MAP_MC_CONNEL
from core.db import get_connection
from core.paths import FILE_NAME

RAW_TABLE = Path(FILE_NAME).stem.replace("-", "_")


def stockpile_usa_hist(series_ids: list[str]) -> pd.DataFrame:
    mapped_series = {v: k for k, v in MAP_MC_CONNEL.items()}

    quoted_series = ", ".join(f"'{mapped_series[s]}'" for s in series_ids)

    query = f"""
        SELECT
            period,
            series_id,
            value
        FROM raw.{RAW_TABLE}
        WHERE series_id IN ({quoted_series})
        """

    with get_connection(read_only=True) as conn:
        df = conn.execute(query).fetchdf()

    df["series_id"] = df["series_id"].map(MAP_MC_CONNEL)

    df = df.pivot(
        index="period",
        columns="series_id",
        values="value",
    ).sort_index()

    return df[series_ids]
