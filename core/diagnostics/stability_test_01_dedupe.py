import psycopg2
import os


def run():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (type, payload, result, status)
        VALUES
        ('test', '{"user_id": 123}', '"msg"'::jsonb, 'done'),
        ('test', '{"user_id": 123}', '"msg"'::jsonb, 'done');
    """)

    conn.commit()

    cur.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE payload->>'user_id' = '123';
    """)

    print("DUPLICATES:", cur.fetchone())

    conn.close()


if __name__ == "__main__":
    print(">>> STABILITY TEST 01 - DEDUPE")
    run()
