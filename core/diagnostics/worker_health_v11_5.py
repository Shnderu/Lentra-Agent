import psycopg2
import os
import socket


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT status, COUNT(*)
        FROM tasks
        GROUP BY status
    """)

    print("QUEUE:", cur.fetchall())

    print("HOST:", socket.gethostname())

    conn.close()


if __name__ == "__main__":
    print(">>> WORKER HEALTH V11.5")
    run()
