# LENTRA DB LAYER (PRODUCTION MODE)

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def load_env():
    env_path = "/opt/lentra/infra/.env"
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    os.environ.setdefault(k, v)

load_env()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def execute(sql, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute(sql, params)
        conn.commit()
        return cur
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
