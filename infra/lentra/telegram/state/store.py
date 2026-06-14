import psycopg2
import json

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

def get_state(user_id: int):
    cur = conn.cursor()
    cur.execute("""
        SELECT state
        FROM user_state
        WHERE user_id = %s
    """, (user_id,))

    row = cur.fetchone()
    cur.close()

    if not row:
        return {}

    return row[0]


def set_state(user_id: int, state: dict):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_state (user_id, state)
        VALUES (%s, %s)
        ON CONFLICT (user_id)
        DO UPDATE SET state = EXCLUDED.state
    """, (user_id, json.dumps(state)))

    conn.commit()
    cur.close()
