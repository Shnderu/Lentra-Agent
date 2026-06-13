import psycopg2
import os

def move_to_dlq(task_id: int, error: str):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'dead',
            result = jsonb_build_object('error', %s),
            updated_at = NOW()
        WHERE id = %s
    """, (error, task_id))

    conn.commit()
    conn.close()
