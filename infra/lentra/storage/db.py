import os
import psycopg2


DB_CONFIG = {
    "dbname": os.getenv("LENTRA_DB_NAME", "lentra"),
    "user": os.getenv("LENTRA_DB_USER", "lentra"),
    "password": os.getenv("LENTRA_DB_PASSWORD", ""),
    "host": os.getenv("LENTRA_DB_HOST", "127.0.0.1"),
    "port": os.getenv("LENTRA_DB_PORT", "5432"),
}


def get_conn():
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
    )


def execute(query, params=None, fetch=False):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            if fetch:
                return cur.fetchall()
            conn.commit()
    finally:
        conn.close()
