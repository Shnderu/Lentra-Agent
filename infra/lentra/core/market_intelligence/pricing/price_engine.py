import psycopg2


def fetch_cluster_stats(cluster_id):
    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        host="127.0.0.1"
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT
            AVG((payload->>'price')::float),
            MIN((payload->>'price')::float),
            MAX((payload->>'price')::float),
            COUNT(*)
        FROM tasks
        WHERE cluster_id = %s
          AND status = 'indexed'
    """, (cluster_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return {
            "avg": None,
            "min": None,
            "max": None,
            "count": 0
        }

    return {
        "avg": row[0],
        "min": row[1],
        "max": row[2],
        "count": row[3]
    }


# ЕДИНЫЙ КОНТРАКТ (СТАБИЛЬНЫЙ)
def compute_price_signal(price, stats):
    avg = stats.get("avg")

    if avg is None:
        return {
            "signal": "neutral",
            "risk": 0.5,
            "delta_vs_market": None
        }

    delta = (price - avg) / avg if avg else 0

    if delta > 0.25:
        signal = "overpriced"
        risk = 0.85
    elif delta > 0.1:
        signal = "slightly_over"
        risk = 0.6
    elif delta < -0.15:
        signal = "underpriced"
        risk = 0.4
    else:
        signal = "fair"
        risk = 0.25

    return {
        "signal": signal,
        "risk": risk,
        "delta_vs_market": delta,
        "market_avg": avg
    }


def update_cluster_stats(cluster_id):
    stats = fetch_cluster_stats(cluster_id)

    conn = psycopg2.connect(
        dbname="lentra",
        user="lentra",
        host="127.0.0.1"
    )
    cur = conn.cursor()

    cur.execute("""
        UPDATE clusters
        SET avg_price = %s,
            min_price = %s,
            max_price = %s,
            listings_count = %s,
            updated_at = NOW()
        WHERE id = %s
    """, (
        stats["avg"],
        stats["min"],
        stats["max"],
        stats["count"],
        cluster_id
    ))

    conn.commit()
    cur.close()
    conn.close()
