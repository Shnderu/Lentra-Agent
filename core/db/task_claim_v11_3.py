import psycopg2
import os

def claim_tasks(limit=10):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload, result
        FROM tasks
        WHERE status = 'done'
        ORDER BY id ASC
        FOR UPDATE SKIP LOCKED
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    task_ids = [r[0] for r in rows]

    if task_ids:
        cur.execute("""
            UPDATE tasks
            SET status = 'processing',
                updated_at = NOW()
            WHERE id = ANY(%s)
        """, (task_ids,))

    conn.commit()
    conn.close()

    return rows
