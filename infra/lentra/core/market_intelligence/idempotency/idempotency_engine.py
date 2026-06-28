import hashlib
import json
from lentra.storage.db import get_conn


def build_idempotency_key(raw_listing: dict) -> str:
    """
    ключ = стабильный хеш источника + id + цена
    """
    base = {
        "id": raw_listing.get("id"),
        "source": raw_listing.get("source"),
        "price": raw_listing.get("price"),
        "title": raw_listing.get("title"),
    }

    raw = json.dumps(base, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def is_processed(key: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM tasks
        WHERE idempotency_key = %s
          AND status = 'done'
        LIMIT 1
    """, (key,))

    exists = cur.fetchone() is not None

    cur.close()
    conn.close()

    return exists


def mark_processed(task_id: str, key: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET idempotency_key = %s
        WHERE id = %s
    """, (key, task_id))

    conn.commit()
    cur.close()
    conn.close()
