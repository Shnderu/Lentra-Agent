# ============================================================
# LENTRA FSM STATE MACHINE V2.2 (CLEAN CHAT-ID CONTRACT)
# ============================================================

import json


def load_state(conn, chat_id):
    cur = conn.cursor()

    cur.execute("""
        SELECT screen, last_event_id, state, version
        FROM user_state
        WHERE chat_id = %s
    """, (chat_id,))

    row = cur.fetchone()

    if not row:
        return {
            "screen": "main",
            "state": {},
            "version": 1
        }

    return {
        "screen": row[0],
        "last_event_id": row[1],
        "state": row[2] or {},
        "version": row[3]
    }


def save_state(conn, chat_id, state, event_id, event):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_state (
            chat_id,
            screen,
            last_event_id,
            state,
            version
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (chat_id)
        DO UPDATE SET
            screen = EXCLUDED.screen,
            last_event_id = EXCLUDED.last_event_id,
            state = EXCLUDED.state,
            version = EXCLUDED.version
    """, (
        chat_id,
        state.get("screen", "main"),
        event_id,
        json.dumps(state.get("state", {})),
        state.get("version", 1)
    ))

    conn.commit()
    cur.close()


def next_state(conn, chat_id, event):
    state = load_state(conn, chat_id)

    new_state = dict(state)

    text = event.get("text", "")

    if "Аренда" in text:
        new_state["screen"] = "rent"
    elif "Поиск" in text:
        new_state["screen"] = "search"
    elif "Профиль" in text:
        new_state["screen"] = "profile"
    else:
        new_state["screen"] = "main"

    event_id = event.get("event_id", "0")

    save_state(conn, chat_id, new_state, event_id, event)

    return new_state
