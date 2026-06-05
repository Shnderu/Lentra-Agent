
import logging
from core.db.connection import get_conn


def add_route(user_id: int, route: str):
    conn = None
    cur = None

    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO routes (user_id, route)
            VALUES (%s, %s)
            """,
            (user_id, route)
        )

        conn.commit()
        return True

    except Exception as e:
        logging.error(f"[DB:add_route] failed: {e}")

        if conn:
            conn.rollback()

        return False

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
