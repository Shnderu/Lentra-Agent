import time
import psycopg2

DB_CONFIG = {
    "host": "db",
    "dbname": "readme_to_recover",
    "user": "postgres",
    "password": "postgres",
}

while True:
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
        print("[DB READY]")
        break
    except Exception as e:
        print("[WAIT DB]", e)
        time.sleep(1)
