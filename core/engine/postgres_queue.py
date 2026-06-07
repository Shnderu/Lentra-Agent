from core.db.connection import get_conn


def claim_tasks(worker_id: str, limit: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, type, payload, retries, max_retries
            FROM public.tasks
            WHERE status = 'new'
            ORDER BY priority DESC, id ASC
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        """, (limit,))

        rows = cur.fetchall()

        if not rows:
            return []

        task_ids = []

        tasks = []

        for row in rows:
            task_id, ttype, payload, retries, max_retries = row

            tasks.append({
                "id": task_id,
                "type": ttype,
                "payload": payload,
                "retries": retries,
                "max_retries": max_retries
            })

            task_ids.append(task_id)

        cur.execute("""
            UPDATE public.tasks
            SET status = 'processing'
            WHERE id = ANY(%s)
        """, (task_ids,))

        return tasks

    finally:
        cur.close()
        conn.close()
