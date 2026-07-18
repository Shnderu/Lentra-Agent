import psycopg2


class TaskFetcher:

    def __init__(self, dsn: str):
        self.dsn = dsn


    def fetch_and_lock(self):

        conn = psycopg2.connect(
            self.dsn
        )

        conn.autocommit = False

        try:

            cur = conn.cursor()

            cur.execute(
                """
                SELECT
                    id,
                    payload,
                    retry_count
                FROM tasks
                WHERE status = 'pending'
                ORDER BY created_at
                FOR UPDATE SKIP LOCKED
                LIMIT 1
                """
            )

            row = cur.fetchone()

            if not row:
                conn.rollback()
                cur.close()
                conn.close()
                return None


            task_id, payload, retry_count = row


            cur.execute(
                """
                UPDATE tasks
                SET status = 'processing'
                WHERE id = %s
                """,
                (
                    task_id,
                )
            )


            conn.commit()

            cur.close()
            conn.close()


            return {
                "id": task_id,
                "payload": payload,
                "retry_count": retry_count
            }


        except Exception:

            conn.rollback()
            conn.close()
            raise
