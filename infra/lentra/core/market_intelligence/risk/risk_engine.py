import psycopg2


def update_risk_score(cluster_id):
    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        host="127.0.0.1"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT AVG((payload->>'price')::float)
        FROM tasks
        WHERE cluster_id = %s
          AND status = 'indexed'
    """, (cluster_id,))

    avg_price = cur.fetchone()[0]

    risk = 0.0

    if avg_price:
        if avg_price > 1200:
            risk = 0.8
        elif avg_price > 800:
            risk = 0.5
        else:
            risk = 0.2

    cur.execute("""
        UPDATE clusters
        SET updated_at = NOW()
        WHERE id = %s
    """, (cluster_id,))

    conn.commit()
    cur.close()
    conn.close()

    return risk
