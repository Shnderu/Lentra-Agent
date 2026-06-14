import psycopg2
import os
import time

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "lentra"),
    "password": os.getenv("DB_PASSWORD", "lentra"),
    "host": "127.0.0.1",
    "port": 5432,
}


def conn():
    c = psycopg2.connect(**DB_CONFIG)
    c.autocommit = True
    return c


def fetch(cur):
    cur.execute("""
        SELECT id, task_type, payload
        FROM public.processing_queue
        WHERE COALESCE(status, 'pending') = 'pending'
        ORDER BY id ASC
        LIMIT 10
    """)
    return cur.fetchall()


def mark_done(cur, task_id):
    cur.execute("""
        UPDATE public.processing_queue
        SET status = 'done'
        WHERE id = %s
    """, (task_id,))


def main():
    print("[WORKER FINAL STARTED]")

    connection = conn()
    cur = connection.cursor()

    while True:
        try:
            tasks = fetch(cur)

            for task_id, task_type, payload in tasks:
                print("[EXEC]", task_id, task_type, payload)

                # временно считаем задачу обработанной
                mark_done(cur, task_id)

            time.sleep(1)

        except Exception as e:
            print("[WORKER ERROR]", e)
            time.sleep(2)


if __name__ == "__main__":
    main()
