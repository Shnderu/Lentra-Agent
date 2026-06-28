import psycopg2
from datetime import datetime, timedelta


class TaskReclaimer:
    """
    Reclaims stuck processing tasks.
    """

    def __init__(self, dsn: str, timeout_seconds: int = 120):
        self.dsn = dsn
        self.timeout = timeout_seconds

    def reclaim(self):
        conn = psycopg2.connect(self.dsn)
        cur = conn.cursor()

        threshold = datetime.utcnow() - timedelta(seconds=self.timeout)

        cur.execute("""
            UPDATE tasks
            SET status = 'pending',
                locked_at = NULL,
                locked_by = NULL
            WHERE status = 'processing'
              AND locked_at < %s
        """, (threshold,))

        affected = cur.rowcount

        conn.commit()
        cur.close()
        conn.close()

        return affected
