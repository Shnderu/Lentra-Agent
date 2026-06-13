import psycopg2
import os

def increase_retry(task_id: int):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET retry_count = COALESCE(retry_count, 0) + 1,
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    conn.close()


def should_dead_letter(retry_count: int, max_retries: int = 5) -> bool:
    return retry_count >= max_retries
