import psycopg2
import os


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM tasks
        GROUP BY status
    """)
    print("QUEUE_STATE:", cur.fetchall())

    cur.execute("""
        SELECT AVG(retry_count)
        FROM tasks
    """)
    print("AVG_RETRY:", cur.fetchone())

    cur.execute("""
        SELECT COUNT(*) FROM tasks WHERE status = 'processing'
    """)
    print("IN_FLIGHT:", cur.fetchone())

    conn.close()


if __name__ == "__main__":
    print(">>> V11.5 QUEUE METRICS")
    run()
