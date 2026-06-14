# ============================================================
# LENTRA QUEUE GUARD V1
# protects consumer from stuck tasks
# ============================================================

import time


def release_stuck_tasks(conn, timeout_sec: int = 60):
    """
    Moves stuck 'processing' tasks back to 'pending'
    """
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'pending'
        WHERE status = 'processing'
        AND updated_at < NOW() - INTERVAL '%s seconds'
    """ % timeout_sec)

    conn.commit()
    cur.close()
