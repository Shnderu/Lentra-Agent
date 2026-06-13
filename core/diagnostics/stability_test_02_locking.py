import os
import psycopg2


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'done'
        WHERE status != 'done';
    """)
    conn.commit()

    cur.execute("""
        SELECT COUNT(*) FROM tasks WHERE status='done';
    """)

    print("READY TASKS:", cur.fetchone())

    conn.close()


if __name__ == "__main__":
    print(">>> STABILITY TEST 02 - LOCKING")
    run()
