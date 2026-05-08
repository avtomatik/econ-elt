from pathlib import Path

import duckdb

from core.db import connect
from core.paths import FILE_NAME

RAW_TABLE = Path(FILE_NAME).stem.replace("-", "_")


def stockpile_usa_hist(series_ids: list[str]) -> duckdb.DuckDBPyRelation:
    quoted_series = ", ".join(f"'{series_id}'" for series_id in series_ids)

    query = f"""
        PIVOT (
            SELECT
                period,
                series_id,
                value
            FROM raw.{RAW_TABLE}
            WHERE series_id IN ({quoted_series})
        )
        ON series_id
        USING FIRST(value)
        ORDER BY period
        """

    conn = connect()

    return conn.sql(query)
