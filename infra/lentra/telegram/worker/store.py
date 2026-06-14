import psycopg2
import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "lentra"),
    "password": os.getenv("DB_PASSWORD", "lentra"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", 5432),
}


def get_conn():
    return psycopg2.connect(**DB_CONFIG)


def fetch_tasks(limit=10):
    conn = get_conn()
    cur = conn.cursor()

    # ❗ FIX: используем реальные поля таблицы
    cur.execute("""
        SELECT id, type, payload
        FROM processing_queue
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def mark_done(task_id, result=None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'done'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


def mark_failed(task_id, error):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'failed'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()
