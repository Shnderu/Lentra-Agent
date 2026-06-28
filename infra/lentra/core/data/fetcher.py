import psycopg2


class TaskFetcher:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def fetch_and_lock(self):
        conn = psycopg2.connect(self.dsn)
        conn.autocommit = False

        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, payload, attempts, max_attempts
                FROM tasks
                WHERE status = 'pending'
                  AND run_after <= now()
                ORDER BY created_at
                FOR UPDATE SKIP LOCKED
                LIMIT 1
            """)

            row = cur.fetchone()

            if not row:
                conn.rollback()
                return None

            task_id, payload, attempts, max_attempts = row

            cur.execute("""
                UPDATE tasks
                SET status = 'processing'
                WHERE id = %s
            """, (task_id,))

            conn.commit()
            cur.close()
            conn.close()

            return task_id, payload, attempts, max_attempts

        except Exception:
            conn.rollback()
            conn.close()
            raise
