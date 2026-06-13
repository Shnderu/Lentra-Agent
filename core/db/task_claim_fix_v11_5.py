import psycopg2
import os


def claim(limit=10):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        WITH cte AS (
            SELECT id
            FROM tasks
            WHERE status = 'done'
            ORDER BY id
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        )
        UPDATE tasks t
        SET status = 'processing'
        FROM cte
        WHERE t.id = cte.id
        RETURNING t.id, t.payload, t.result;
    """, (limit,))

    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return rows
