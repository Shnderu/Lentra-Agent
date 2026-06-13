import time
import psycopg2
import json
import os

from lentra.domain.vietnam_rent_engine import search_vietnam_properties
from lentra.ux.pipeline import build_user_response

DB = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432"))
}

def get_conn():
    return psycopg2.connect(**DB)

def fetch(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status='new'
        FOR UPDATE SKIP LOCKED
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    return rows

def process(task):
    task_id, task_type, payload = task

    if task_type == "search_property_vietnam":
        items = payload if isinstance(payload, list) else []
        result = build_user_response(items)
    else:
        result = f"unknown task: {task_type}"

    return result

def mark(conn, task_id, result):
    cur = conn.cursor()
    cur.execute("""
        UPDATE processing_queue
        SET status='done',
            processed_at=NOW(),
            result=%s
        WHERE id=%s
    """, (json.dumps({"message": result}), task_id))
    cur.close()

def main():
    conn = get_conn()
    conn.autocommit = False

    print("[UX WORKER] started")

    while True:
        try:
            batch = fetch(conn)

            if not batch:
                conn.commit()
                time.sleep(0.3)
                continue

            for task in batch:
                task_id = task[0]

                try:
                    result = process(task)
                    mark(conn, task_id, result)
                    print(f"[DONE UX] {task_id}")

                except Exception as e:
                    print(f"[ERROR] {task_id}: {e}")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"[FATAL]: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
