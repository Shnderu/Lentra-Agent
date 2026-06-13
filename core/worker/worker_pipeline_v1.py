import json
import os
import psycopg2

from core.task_contract.repository import TaskRepository
from core.task_contract.state_machine import can_transition


class WorkerPipeline:

    def __init__(self):
        self.repo = TaskRepository(os.getenv("DATABASE_URL"))

    def run_once(self, handler_map: dict):

        conn = self.repo.get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, type, payload, status
            FROM tasks
            WHERE status = 'pending'
            ORDER BY id
            LIMIT 10
            FOR UPDATE SKIP LOCKED
        """)

        tasks = cur.fetchall()

        for task_id, task_type, payload, status in tasks:

            try:
                if isinstance(payload, str):
                    payload = json.loads(payload)

                handler = handler_map.get(task_type)

                if not handler:
                    raise Exception(f"No handler for {task_type}")

                if not can_transition(status, "processing"):
                    continue

                cur.execute("""
                    UPDATE tasks
                    SET status = 'processing',
                        updated_at = NOW()
                    WHERE id = %s
                """, (task_id,))

                result = handler(payload)

                cur.execute("""
                    UPDATE tasks
                    SET status = 'done',
                        result = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (json.dumps(result), task_id))

            except Exception as e:

                cur.execute("""
                    UPDATE tasks
                    SET status = 'failed',
                        error = %s,
                        updated_at = NOW()
                    WHERE id = %s
                """, (str(e), task_id))

        conn.commit()
        conn.close()
