import uuid

class TaskQueueRepository:
    def __init__(self, db):
        self.db = db

    def enqueue(self, task_type: str, payload: dict):
        task_id = str(uuid.uuid4())

        self.db.execute("""
            INSERT INTO task_queue (id, type, payload)
            VALUES (%s, %s, %s)
        """, (task_id, task_type, payload))

        return task_id

    def fetch_next(self, worker_id: str):
        return self.db.fetch_one("""
            SELECT *
            FROM task_queue
            WHERE status = 'pending'
              AND run_after <= now()
            ORDER BY created_at
            FOR UPDATE SKIP LOCKED
            LIMIT 1
        """)

    def lock(self, task_id: str, worker_id: str):
        self.db.execute("""
            UPDATE task_queue
            SET status='processing',
                locked_at=now(),
                locked_by=%s
            WHERE id=%s
        """, (worker_id, task_id))

    def done(self, task_id: str):
        self.db.execute("""
            UPDATE task_queue
            SET status='done',
                updated_at=now()
            WHERE id=%s
        """, (task_id,))

    def fail(self, task_id: str):
        self.db.execute("""
            UPDATE task_queue
            SET attempts = attempts + 1,
                status = CASE
                    WHEN attempts + 1 >= max_attempts THEN 'failed'
                    ELSE 'pending'
                END,
                run_after = now() + interval '30 seconds',
                updated_at=now()
            WHERE id=%s
        """, (task_id,))
