import psycopg2
import os

def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT status, count(*)
        FROM tasks
        GROUP BY status
    """)

    print("TASK STATUS:", cur.fetchall())

    conn.close()


if __name__ == "__main__":
    print(">>> WORKER HEALTH V11.2")
    run()
