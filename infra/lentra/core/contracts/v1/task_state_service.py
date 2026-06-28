import json
from lentra.storage.db import get_conn
from lentra.core.contracts.v1.task_state import TaskState, can_transition


class TaskStateService:

    def transition(self, task_id: str, from_state: str, to_state: str, meta: dict = None):
        if not can_transition(from_state, to_state):
            raise ValueError(f"[STATE] invalid transition {from_state} → {to_state}")

        conn = get_conn()
        cur = conn.cursor()

        payload_patch = json.dumps(meta or {})

        cur.execute("""
            UPDATE tasks
            SET status = %s,
                payload = payload || %s
            WHERE id = %s
        """, (to_state, payload_patch, task_id))

        conn.commit()
        cur.close()
        conn.close()

    def set_status(self, task_id: str, status: str, meta: dict = None):
        conn = get_conn()
        cur = conn.cursor()

        payload_patch = json.dumps(meta or {})

        cur.execute("""
            UPDATE tasks
            SET status = %s,
                payload = payload || %s
            WHERE id = %s
        """, (status, payload_patch, task_id))

        conn.commit()
        cur.close()
        conn.close()
