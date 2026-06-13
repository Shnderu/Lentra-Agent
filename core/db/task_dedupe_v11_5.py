import hashlib
import psycopg2
import os


def fingerprint(payload: dict) -> str:
    raw = str(sorted(payload.items())).encode()
    return hashlib.sha256(raw).hexdigest()


def is_duplicate(fp: str) -> bool:
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM tasks
        WHERE fingerprint = %s
        LIMIT 1
    """, (fp,))

    exists = cur.fetchone() is not None
    conn.close()
    return exists
