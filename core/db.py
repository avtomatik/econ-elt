import logging
from contextlib import contextmanager

import duckdb

from core.paths import DATA_DIR, WAREHOUSE_NAME

logger = logging.getLogger(__name__)


@contextmanager
def get_connection(read_only: bool = False):
    conn = duckdb.connect(
        database=str(DATA_DIR / "processed" / WAREHOUSE_NAME),
        read_only=read_only,
    )

    try:
        yield conn
        conn.commit()

    except Exception as exc:
        logger.exception("Database connection failed.")
        conn.rollback()
        raise exc

    finally:
        conn.close()
