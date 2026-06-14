import psycopg2
import json
import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "lentra"),
    "password": os.getenv("DB_PASSWORD", "lentra"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": 5432,
}


def conn():
    return psycopg2.connect(**DB_CONFIG)


def get_state(chat_id: int) -> dict:
    c = conn()
    cur = c.cursor()

    cur.execute("""
        SELECT state
        FROM user_state
        WHERE chat_id = %s
    """, (chat_id,))

    row = cur.fetchone()

    cur.close()
    c.close()

    if not row:
        return {"screen": "main", "step": None, "data": {}}

    return row[0]


def set_state(chat_id: int, state: dict):
    c = conn()
    cur = c.cursor()

    cur.execute("""
        INSERT INTO user_state (chat_id, state, updated_at)
        VALUES (%s, %s, NOW())
        ON CONFLICT (chat_id)
        DO UPDATE SET
            state = EXCLUDED.state,
            updated_at = NOW()
    """, (chat_id, json.dumps(state)))

    c.commit()
    cur.close()
    c.close()

import datetime


def log_transition(chat_id: int, old_state: dict, new_state: dict):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS state_log (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                old_state JSONB,
                new_state JSONB,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        cur.execute("""
            INSERT INTO state_log (chat_id, old_state, new_state)
            VALUES (%s, %s, %s)
        """, (chat_id, json.dumps(old_state), json.dumps(new_state)))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print("[STATE LOG ERROR]", e)
