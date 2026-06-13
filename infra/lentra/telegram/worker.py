# LENTRA WORKER (STABLE SQL FIX)

import time
from lentra.storage.db import get_conn

print("[WORKER] started")

def process():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, raw_message_id
            FROM processing_queue
            WHERE status='new'
            ORDER BY id ASC
            LIMIT 20
        """)
        rows = cur.fetchall()

        for r in rows:
            task_id = r[0]
            trace_id = r[1]

            try:
                cur.execute("""
                    UPDATE processing_queue
                    SET status = 'done',
                        processed_at = NOW()
                    WHERE id = %s
                """, (task_id,))

                conn.commit()
                print(f"[WORKER] DONE trace={trace_id}")

            except Exception as e:
                conn.rollback()
                print(f"[WORKER ERROR] trace={trace_id}: {e}")

    finally:
        cur.close()
        conn.close()

def main():
    while True:
        process()
        time.sleep(1)

if __name__ == "__main__":
    main()
