import time
import psycopg2

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[DISPATCHER PROD] STARTED")


def fetch_new():
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status = 'new'
        ORDER BY id
        LIMIT 20
    """)

    rows = cur.fetchall()
    cur.close()

    return rows


def mark_processing(task_id):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET
            status = 'processing',
            started_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()


def main():
    while True:

        tasks = fetch_new()

        for task_id, task_type, payload in tasks:

            mark_processing(task_id)

            print(
                f"[DISPATCH] "
                f"id={task_id} "
                f"type={task_type}"
            )

        time.sleep(0.3)


if __name__ == "__main__":
    main()
