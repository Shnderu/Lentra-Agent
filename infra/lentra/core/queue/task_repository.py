import uuid
import json
import psycopg2


class TaskRepository:

    def __init__(self, dsn: str):
        self.dsn = dsn

    def push(self, payload: dict) -> str:
        task_id = str(uuid.uuid4())

        conn = psycopg2.connect(self.dsn)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO tasks (id, payload, status) VALUES (%s, %s, %s)",
            (task_id, json.dumps(payload), "pending")
        )

        conn.commit()
        cur.close()
        conn.close()

        return task_id

    def fetch_next(self):
        conn = psycopg2.connect(self.dsn)
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload
            FROM tasks
            WHERE status = 'pending'
            ORDER BY created_at ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """)

        row = cur.fetchone()

        if not row:
            conn.close()
            return None

        task_id, payload = row

        cur.execute(
            "UPDATE tasks SET status = 'processing' WHERE id = %s",
            (task_id,)
        )

        conn.commit()
        cur.close()
        conn.close()

        return task_id, payload

    def mark_done(self, task_id: str, result: dict):
        conn = psycopg2.connect(self.dsn)
        cur = conn.cursor()

        cur.execute(
            "UPDATE tasks SET status = 'done', payload = payload || %s WHERE id = %s",
            (json.dumps({"result": result}), task_id)
        )

        conn.commit()
        conn.close()

    def mark_failed(self, task_id: str, error: str):
        conn = psycopg2.connect(self.dsn)
        cur = conn.cursor()

        cur.execute(
            "UPDATE tasks SET status = 'failed', payload = payload || %s WHERE id = %s",
            (json.dumps({"error": error}), task_id)
        )

        conn.commit()
        conn.close()
