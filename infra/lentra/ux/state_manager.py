import psycopg2
import json
import os


DB = {
    "dbname": os.getenv("DB_NAME", "lentra"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "5432"))
}


def get_conn():
    return psycopg2.connect(**DB)


def load_state(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT last_intent, last_scenario, context
        FROM user_state
        WHERE user_id = %s
    """, (user_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return {
            "last_intent": None,
            "last_scenario": None,
            "context": {}
        }

    return {
        "last_intent": row[0],
        "last_scenario": row[1],
        "context": row[2] or {}
    }


def save_state(user_id, intent, scenario, context):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_state (user_id, last_intent, last_scenario, context, updated_at)
        VALUES (%s, %s, %s, %s, NOW())
        ON CONFLICT (user_id)
        DO UPDATE SET
            last_intent = EXCLUDED.last_intent,
            last_scenario = EXCLUDED.last_scenario,
            context = EXCLUDED.context,
            updated_at = NOW()
    """, (
        user_id,
        intent,
        scenario,
        json.dumps(context)
    ))

    conn.commit()
    cur.close()
    conn.close()
