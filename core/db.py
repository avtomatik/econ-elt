import logging
from contextlib import contextmanager

import duckdb

from core.paths import DATA_DIR, WAREHOUSE_NAME

logger = logging.getLogger(__name__)


def connect(read_only: bool = False) -> duckdb.DuckDBPyConnection:
    return duckdb.connect(
        database=str(DATA_DIR / "processed" / WAREHOUSE_NAME),
        read_only=read_only,
    )


@contextmanager
def get_connection(read_only: bool = False):

    conn = connect(read_only)

    try:
        yield conn

    except Exception:
        logger.exception("Database connection failed.")
        raise

    finally:
        conn.close()
