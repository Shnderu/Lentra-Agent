import time
import psycopg2

DB_CONFIG = {
    "host": "db",
    "dbname": "readme_to_recover",
    "user": "postgres",
    "password": "postgres",
}


def wait_schema(timeout: int = 30):
    start = time.time()

    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()

            # фиксируем schema
            cur.execute("SET search_path TO public;")

            # проверка таблицы
            cur.execute("""
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = 'tasks'
            """)

            ok = cur.fetchone()

            conn.close()

            if ok:
                print("[BOOT] SCHEMA READY")
                return True

        except Exception as e:
            print("[BOOT] schema check failed:", e)

        if time.time() - start > timeout:
            raise RuntimeError("Schema not ready (timeout)")

        time.sleep(2)
