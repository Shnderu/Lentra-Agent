from lentra.storage.db import get_conn


def get_cluster_listings(cluster_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload, status
        FROM tasks
        WHERE cluster_id = %s
          AND status = 'done'
    """, (cluster_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
