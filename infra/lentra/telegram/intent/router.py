# ============================================================
# LENTRA ROUTER V2.1 (FSM ADAPTER FIXED)
# ============================================================

from lentra.telegram.state.machine import next_state
from lentra.telegram.db import get_conn


def route(payload: dict):
    chat_id = payload.get("chat_id")
    event = payload

    if not chat_id:
        return {
            "screen": "main",
            "state": {}
        }

    conn = get_conn()

    state = next_state(conn, chat_id, event)

    return state
