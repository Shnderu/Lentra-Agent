import uuid
from datetime import datetime

class TasksRepository:
    def __init__(self, db):
        self.db = db

    def fetch_next(self):
        return self.db.fetch_one("""
            SELECT *
            FROM tasks
            WHERE status = 'pending'
            ORDER BY created_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        """)

    def mark_processing(self, task_id: str, worker_id: str):
        self.db.execute("""
            UPDATE tasks
            SET status='processing',
                locked_at=now(),
                locked_by=%s
            WHERE id=%s
        """, (worker_id, task_id))

    def mark_done(self, task_id: str):
        self.db.execute("""
            UPDATE tasks
            SET status='done',
                updated_at=now()
            WHERE id=%s
        """, (task_id,))

    def mark_failed(self, task_id: str):
        self.db.execute("""
            UPDATE tasks
            SET attempts = attempts + 1,
                status = CASE
                    WHEN attempts + 1 >= max_attempts THEN 'failed'
                    ELSE 'pending'
                END,
                updated_at=now()
            WHERE id=%s
        """, (task_id,))
