import psycopg2
import json
from typing import Dict, Any, Optional


conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)


def get_session(chat_id: int) -> Dict[str, Any]:
    cur = conn.cursor()
    cur.execute("""
        SELECT state
        FROM telegram_sessions
        WHERE chat_id = %s
    """, (chat_id,))

    row = cur.fetchone()
    cur.close()

    if not row:
        return {
            "chat_id": chat_id,
            "stack": [],
            "data": {}
        }

    return row[0]


def save_session(chat_id: int, state: Dict[str, Any]):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO telegram_sessions (chat_id, state)
        VALUES (%s, %s::jsonb)
        ON CONFLICT (chat_id)
        DO UPDATE SET state = EXCLUDED.state
    """, (chat_id, json.dumps(state)))
    conn.commit()
    cur.close()
