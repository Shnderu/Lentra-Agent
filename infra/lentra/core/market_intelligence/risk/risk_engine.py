

def update_risk_score(listing, cluster_stats=None):

    score = 0.5  # base risk

    price = listing.get("price")

    if isinstance(price, dict):
        price = price.get("value", 0)

    # PRICE ANOMALY
    if cluster_stats:
        if price and price < cluster_stats.get("min_price", price):
            score += 0.2

    # DATA COMPLETENESS
    if not listing.get("location"):
        score += 0.1

    if not listing.get("features"):
        score += 0.1

    # CLUSTER RISK
    if cluster_stats and cluster_stats.get("listings_count", 0) > 5:
        score += 0.1

    # clamp
    score = max(0.0, min(1.0, score))

    if score > 0.7:
        label = "high_risk"
    elif score > 0.4:
        label = "medium_risk"
    else:
        label = "low_risk"

    return {
        "risk_score": round(score, 3),
        "risk_level": label
    }
