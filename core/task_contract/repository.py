import psycopg2


class TaskRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def get_conn(self):
        return psycopg2.connect(self.dsn)

    def fetch_done(self, limit=10):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload, result, status
            FROM tasks
            WHERE status = 'done'
            ORDER BY id ASC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        conn.close()
        return rows

    def mark_sent(self, task_id: int):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'sent',
                updated_at = NOW()
            WHERE id = %s
        """, (task_id,))

        conn.commit()
        conn.close()
EOFcat << 'EOF' > /opt/lentra/core/task_contract/repository.py
import psycopg2


class TaskRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def get_conn(self):
        return psycopg2.connect(self.dsn)

    def fetch_done(self, limit=10):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, payload, result, status
            FROM tasks
            WHERE status = 'done'
            ORDER BY id ASC
            LIMIT %s
        """, (limit,))

        rows = cur.fetchall()
        conn.close()
        return rows

    def mark_sent(self, task_id: int):
        conn = self.get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status = 'sent',
                updated_at = NOW()
            WHERE id = %s
        """, (task_id,))

        conn.commit()
        conn.close()
