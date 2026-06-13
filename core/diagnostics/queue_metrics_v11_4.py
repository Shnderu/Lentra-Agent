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
    print("QUEUE STATE:", cur.fetchall())

    cur.execute("""
        SELECT AVG(retry_count)
        FROM tasks
    """)
    print("AVG RETRY:", cur.fetchone())

    conn.close()


if __name__ == "__main__":
    print(">>> QUEUE METRICS V11.4")
    run()
