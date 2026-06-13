import psycopg2
import os


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM tasks
        GROUP BY status;
    """)

    print("QUEUE STATE:", cur.fetchall())

    cur.execute("""
        SELECT COUNT(*) FROM tasks;
    """)

    print("TOTAL TASKS:", cur.fetchone())

    conn.close()


if __name__ == "__main__":
    print(">>> STABILITY TEST 05 - METRICS")
    run()
