import os
import psycopg2


def get_conn():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )

    conn.autocommit = False

    # 🔥 ЖЁСТКО ПРИВЯЗЫВАЕМСЯ К СХЕМЕ
    with conn.cursor() as cur:
        cur.execute("SET search_path TO public")

    return conn
