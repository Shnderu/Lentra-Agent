import time
import psycopg2

DB = {
    "host": "db",
    "dbname": "readme_to_recover",
    "user": "postgres",
    "password": "postgres"
}

def wait_db():
    while True:
        try:
            conn = psycopg2.connect(**DB)
            conn.close()
            print("[BOOT] DB READY")
            return
        except Exception as e:
            print("[BOOT WAIT]", e)
            time.sleep(1)

wait_db()
