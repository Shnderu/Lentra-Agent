import psycopg2
import json
from typing import Optional, List, Tuple


class TaskRepository:

    def __init__(self, dsn: str):
        self.dsn = dsn

    def get_conn(self):
        return psycopg2.connect(self.dsn)

    def claim_tasks(self, limit: int = 10) -> List[Tuple]:
        """
        Атомарный захват задач (anti-duplication safe)
        """

        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'processing',
                updated_at = NOW()
            WHERE id IN (
                SELECT id
                FROM tasks
                WHERE status = 'pending'
                ORDER BY id ASC
                FOR UPDATE SKIP LOCKED
                LIMIT %s
            )
            RETURNING id, type, payload;
        """, (limit,))

        rows = cur.fetchall()
        conn.commit()
        conn.close()

        return rows

    def mark_done(self, task_id: int, result: dict):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'done',
                result = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (json.dumps(result), task_id))

        conn.commit()
        conn.close()

    def mark_failed(self, task_id: int, error: str):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'failed',
                error = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (error, task_id))

        conn.commit()
        conn.close()
