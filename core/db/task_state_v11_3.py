import psycopg2
import os

def mark_sent(task_id):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'sent',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    conn.close()


def mark_failed(task_id):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'failed',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    conn.close()
