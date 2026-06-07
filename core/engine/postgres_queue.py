import os
import psycopg2


def get_conn():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
    )

    conn.autocommit = False

    return conn


def _ensure_schema(cur):
    cur.execute("SET search_path TO public")


def claim_tasks(worker_id: str, limit: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    try:
        _ensure_schema(cur)

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
            conn.commit()
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
            SET status='processing'
            WHERE id = ANY(%s)
        """, (task_ids,))

        conn.commit()
        return tasks

    except Exception as e:
        conn.rollback()
        print(f"[CLAIM ERROR] {e}")
        return []

    finally:
        cur.close()
        conn.close()


def mark_done(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    try:
        _ensure_schema(cur)

        cur.execute("""
            UPDATE public.tasks
            SET status='done'
            WHERE id=%s
        """, (task_id,))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"[DONE ERROR] {e}")

    finally:
        cur.close()
        conn.close()


def mark_failed(task: dict):
    conn = get_conn()
    cur = conn.cursor()

    try:
        _ensure_schema(cur)

        new_retry = task["retries"] + 1
        status = "failed" if new_retry >= task["max_retries"] else "new"

        cur.execute("""
            UPDATE public.tasks
            SET status=%s,
                retries=%s
            WHERE id=%s
        """, (status, new_retry, task["id"]))

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"[FAIL ERROR] {e}")

    finally:
        cur.close()
        conn.close()
