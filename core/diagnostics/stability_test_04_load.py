import psycopg2
import os


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    for i in range(50):
        cur.execute("""
            INSERT INTO tasks (type, payload, result, status)
            VALUES (
                'load',
                %s,
                '"load test"'::jsonb,
                'done'
            )
        """, (f'{{"user_id": 928857415, "i": {i}}}',))

    conn.commit()
    conn.close()

    print("LOAD TEST INSERTED 50 TASKS")


if __name__ == "__main__":
    print(">>> STABILITY TEST 04 - LOAD")
    run()
