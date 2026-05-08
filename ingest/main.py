import logging
from pathlib import Path

from core.db import get_connection
from core.paths import DATA_DIR

logging.basicConfig(level=logging.INFO)


def ingest_parquet_to_duckdb(parquet_path: Path, table_name: str):

    with get_connection() as conn:

        conn.execute("""CREATE SCHEMA IF NOT EXISTS raw;""")

        conn.execute(
            f"""
            CREATE OR REPLACE TABLE raw.{table_name} AS
            SELECT *
            FROM read_parquet('{parquet_path}');
            """
        )

        logging.info(f"Finished ingesting {table_name}.")


def main():
    for parquet_file in (DATA_DIR / "raw").glob("*.parquet"):
        table_name = parquet_file.stem.replace("-", "_")
        ingest_parquet_to_duckdb(parquet_file, table_name)


if __name__ == "__main__":
    main()
