import time
import logging
import psycopg2
import psutil

# ---------------- CONFIG ----------------
WORKER_ID = "worker-1"

MAX_CPU = 75.0
IDLE_SLEEP = 0.5
WORK_SLEEP = 0.15
OVERLOAD_SLEEP = 1.0

logging.basicConfig(level=logging.INFO)

# ---------------- DB ----------------
conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="***",
    host="127.0.0.1",
    port=5432
)
conn.autocommit = False


def get_task_from_db():
    with conn.cursor() as cur:
        cur.execute("""
        WITH cte AS (
            SELECT id
            FROM tasks
            WHERE status = 'pending'
            ORDER BY created_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        )
        UPDATE tasks t
        SET status = 'processing'
        FROM cte
        WHERE t.id = cte.id
        RETURNING t.id, t.payload;
        """)
        row = cur.fetchone()
        return row


def process_task(task):
    # TODO: replace with real pipeline logic
    time.sleep(0.05)


def cpu_ok():
    return psutil.cpu_percent(interval=0.1) < MAX_CPU


def run():
    logging.info(f"[{WORKER_ID}] started linear worker")

    while True:

        if not cpu_ok():
            logging.warning(f"[{WORKER_ID}] CPU overload → backoff")
            time.sleep(OVERLOAD_SLEEP)
            continue

        task = get_task_from_db()

        if not task:
            time.sleep(IDLE_SLEEP)
            continue

        try:
            process_task(task)
        except Exception as e:
            logging.error(f"[{WORKER_ID}] task error: {e}")

        time.sleep(WORK_SLEEP)


if __name__ == "__main__":
    run()
