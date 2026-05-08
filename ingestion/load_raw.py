import logging

import duckdb
import yaml


logging.basicConfig(level=logging.INFO)


def load_config():
    with open("config/pipeline.yml", "r") as f:
        return yaml.safe_load(f)


def connect(db_path: str):
    return duckdb.connect(db_path)


def ingest_parquet(conn, file_path: str, table_name: str):
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    conn.execute(f"""
        CREATE OR REPLACE TABLE raw.{table_name} AS
        SELECT * FROM read_parquet('{file_path}')
    """)

    logging.info(f"Loaded raw.{table_name}")


def main():
    config = load_config()

    db_path = config["warehouse"]["database"]
    conn = connect(db_path)

    for source_name, source in config["sources"].items():
        ingest_parquet(conn, source["file"], source["table"])

    conn.close()


if __name__ == "__main__":
    main()



