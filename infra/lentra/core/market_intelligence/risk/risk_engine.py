from lentra.core.market_intelligence.repository.cluster_repository import get_cluster_listings


def update_risk_score(cluster_id: str):
    rows = get_cluster_listings(cluster_id)

    prices = []
    for _, payload, _ in rows:
        if isinstance(payload, dict) and payload.get("price"):
            prices.append(float(payload["price"]))

    if not prices:
        return

    avg_price = sum(prices) / len(prices)

    if avg_price < 300:
        risk = 0.2
    elif avg_price < 800:
        risk = 0.5
    else:
        risk = 0.8

    from lentra.storage.db import get_conn
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE clusters
        SET risk_score = %s
        WHERE id = %s
    """, (risk, cluster_id))

    conn.commit()
    cur.close()
    conn.close()
