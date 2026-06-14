import psycopg2
import json
import hashlib
from lentra.telegram.db import get_conn


def _event_hash(event: dict) -> str:
    raw = json.dumps(event, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def load_state(conn, chat_id: int):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT screen, last_event_id, state, version
            FROM user_state
            WHERE chat_id = %s
        """, (chat_id,))
        row = cur.fetchone()

    if not row:
        return {
            "screen": "main",
            "last_event_id": None,
            "state": {},
            "version": 1
        }

    return {
        "screen": row[0],
        "last_event_id": row[1],
        "state": row[2] or {},
        "version": row[3]
    }


def save_state(conn, chat_id: int, new_state: dict, event_id: str, event: dict):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_state (chat_id, screen, last_event_id, state, version, updated_at)
            VALUES (%s, %s, %s, %s, 1, NOW())
            ON CONFLICT (chat_id) DO UPDATE SET
                screen = EXCLUDED.screen,
                last_event_id = EXCLUDED.last_event_id,
                state = EXCLUDED.state,
                version = user_state.version + 1,
                updated_at = NOW()
        """, (
            chat_id,
            new_state["screen"],
            event_id,
            json.dumps(new_state.get("state", {}))
        ))

    conn.commit()


def next_state(chat_id: int, event: dict):
    conn = get_conn()

    try:
        state = load_state(conn, chat_id)

        event_id = _event_hash(event)

        # 🔥 DEDUPLICATION
        if state["last_event_id"] == event_id:
            print("[FSM] duplicate event ignored")
            return state

        text = event.get("text", "")

        screen = state["screen"]

        # 🔵 SIMPLE TRANSITIONS (A+ BASE)
        if text == "/start":
            screen = "main"

        elif "Аренда" in text:
            screen = "rent"

        elif "Поиск" in text:
            screen = "search"

        elif "Профиль" in text:
            screen = "profile"

        elif "Уведомления" in text:
            screen = "notifications"

        # fallback safety
        if not screen:
            screen = "main"

        new_state = {
            "screen": screen,
            "state": state["state"]
        }

        save_state(conn, chat_id, new_state, event_id, event)

        return new_state

    finally:
        conn.close()
