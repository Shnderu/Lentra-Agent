import time
import json
from typing import Optional, Dict, Any

import psycopg2
from psycopg2.extras import RealDictCursor


class TaskClaimError(Exception):
    pass


class TaskClaimer:
    """
    PostgreSQL-based atomic task claim system.

    Strategy:
    - SELECT ... FOR UPDATE SKIP LOCKED
    - minimal locking window
    - no external queue dependency
    """

    def __init__(self, dsn: str):
        self.dsn = dsn

    def _connect(self):
        return psycopg2.connect(self.dsn)

    def claim(self, worker_id: str, task_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Atomically claim one pending task.
        """

        query_base = """
            SELECT *
            FROM tasks
            WHERE status = 'pending'
        """

        params = []

        if task_type:
            query_base += " AND type = %s"
            params.append(task_type)

        query_base += """
            ORDER BY created_at ASC
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        """

        with self._connect() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("BEGIN;")

                cur.execute(query_base, params)
                task = cur.fetchone()

                if not task:
                    conn.commit()
                    return None

                cur.execute(
                    """
                    UPDATE tasks
                    SET status = 'processing',
                        locked_by = %s,
                        locked_at = NOW(),
                        attempts = COALESCE(attempts, 0) + 1
                    WHERE id = %s
                    """,
                    (worker_id, task["id"])
                )

                conn.commit()

                return dict(task)

    def mark_done(self, task_id: str, result: dict):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tasks
                    SET status = 'done',
                        result = %s,
                        finished_at = NOW()
                    WHERE id = %s
                    """,
                    (json.dumps(result), task_id)
                )
                conn.commit()

    def mark_failed(self, task_id: str, error: str):
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE tasks
                    SET status = 'failed',
                        error = %s,
                        finished_at = NOW()
                    WHERE id = %s
                    """,
                    (error, task_id)
                )
                conn.commit()
