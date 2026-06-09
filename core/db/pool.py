import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

_minconn = int(os.getenv("DB_POOL_MIN", "1"))
_maxconn = int(os.getenv("DB_POOL_MAX", "10"))

_pool = ThreadedConnectionPool(
    minconn=_minconn,
    maxconn=_maxconn,
    **DB_CONFIG
)


def get_conn():
    """
    Acquire connection from pool.
    """
    return _pool.getconn()


def put_conn(conn):
    """
    Return connection back to pool.
    """
    if conn:
        _pool.putconn(conn)


def execute(query, params=None, fetch=False):
    """
    Safe helper for simple queries.
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(query, params)

        if fetch:
            result = cur.fetchall()
        else:
            result = None

        conn.commit()
        cur.close()
        return result

    finally:
        put_conn(conn)
