import psycopg2
import os

def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM tasks;")
    print("TASKS:", cur.fetchone())

    cur.execute("SELECT status, count(*) FROM tasks GROUP BY status;")
    print("STATS:", cur.fetchall())

    conn.close()

if __name__ == "__main__":
    print(">>> V11.1 CHECK")
    run()
