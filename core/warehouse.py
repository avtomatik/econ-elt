from pathlib import Path

import pandas as pd

from core.db import get_connection
from core.paths import FILE_NAME

RAW_TABLE = Path(FILE_NAME).stem.replace("-", "_")


def stockpile_usa_hist(series_ids: list[str]) -> pd.DataFrame:
    quoted_series = ", ".join(f"'{s}'" for s in series_ids)

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

    if df.empty:
        raise ValueError(f"Neither of {series_ids} are in warehouse.")

    return df.pivot(
        index="period",
        columns="series_id",
        values="value",
    ).sort_index()[series_ids]
