from lentra.core.market_intelligence.repository.cluster_repository import get_cluster_listings


def update_cluster_stats(cluster_id: str):
    rows = get_cluster_listings(cluster_id)

    prices = []
    for _, payload, _ in rows:
        if isinstance(payload, dict):
            p = payload.get("price")
        else:
            continue

        if p is not None:
            prices.append(float(p))

    if not prices:
        return

    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)

    from lentra.storage.db import get_conn
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE clusters
        SET avg_price = %s,
            min_price = %s,
            max_price = %s,
            listings_count = %s
        WHERE id = %s
    """, (avg_price, min_price, max_price, len(prices), cluster_id))

    conn.commit()
    cur.close()
    conn.close()
