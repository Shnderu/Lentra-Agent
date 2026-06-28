

def compute_scam_score(listing, cluster_stats, price_trend):

    score = 0.0

    price = listing["price"]

    # 1. PRICE ANOMALY
    if cluster_stats:
        if price < cluster_stats["min_price"] * 0.7:
            score += 0.4

    # 2. REPOST / DUPLICATES
    if cluster_stats and cluster_stats["listings_count"] > 5:
        score += 0.2

    # 3. PRICE VOLATILITY
    if price_trend == "dropping":
        score += 0.2

    # 4. MISSING DATA
    if not listing.get("location"):
        score += 0.1

    if not listing.get("features"):
        score += 0.1

    return {
        "scam_score": round(min(score, 1.0), 3),
        "risk_level": (
            "high" if score > 0.6 else
            "medium" if score > 0.3 else
            "low"
        )
    }
