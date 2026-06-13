import time
import psycopg2
import json
from lentra.storage.db import get_conn


def fetch_tasks(conn, limit=5):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status = 'new'
        ORDER BY id
        LIMIT %s
        FOR UPDATE SKIP LOCKED
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    return rows


def mark_processing(conn, task_id):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'processing',
            locked_at = NOW(),
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()


def main():
    print("[DISPATCHER] STARTED")

    while True:
        conn = get_conn()
        tasks = fetch_tasks(conn)

        for task_id, task_type, payload in tasks:

            mark_processing(conn, task_id)

            job = {
                "id": task_id,
                "type": task_type,
                "payload": payload
            }

            print("[DISPATCHER] SEND JOB:", json.dumps(job))

        conn.close()
        time.sleep(1)


if __name__ == "__main__":
    main()
