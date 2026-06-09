from core.engine.postgres_queue import get_connection

def recover_orphan_tasks():
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE tasks
            SET status = 'pending',
                worker_id = NULL,
                locked_at = NULL,
                lease_until = NULL
            WHERE status = 'processing'
              AND lease_until < NOW();
        """)

    conn.close()
