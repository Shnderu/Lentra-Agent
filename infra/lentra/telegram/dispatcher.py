import time
import psycopg2

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

conn.autocommit = True

print("[DISPATCHER FIX FINAL] STARTED")

while True:
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT id
            FROM processing_queue
            WHERE status = 'new'
            ORDER BY id
            LIMIT 10
            FOR UPDATE SKIP LOCKED
        """)

        rows = cur.fetchall()

        if rows:
            ids = [r[0] for r in rows]

            cur.execute("""
                UPDATE processing_queue
                SET status = 'processing'
                WHERE id = ANY(%s)
            """, (ids,))

            print(f"[DISPATCHER] moved_to_processing={len(ids)}")

        cur.close()

    except Exception as e:
        print("[DISPATCHER ERROR]", e)

    time.sleep(0.3)
