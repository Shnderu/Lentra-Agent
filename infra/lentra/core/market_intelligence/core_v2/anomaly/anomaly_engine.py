

def detect_anomaly(listing, cluster_stats, city_stats):

    price = listing.price
    cluster_avg = cluster_stats.get("avg_price", price)
    city_avg = city_stats.get("avg_price", price)

    # deviation from cluster
    cluster_dev = (price - cluster_avg) / cluster_avg if cluster_avg else 0

    # deviation from city
    city_dev = (price - city_avg) / city_avg if city_avg else 0

    risk_score = 0.5

    # rules-based anomaly detection
    if abs(cluster_dev) > 0.5:
        risk_score += 0.3

    if abs(city_dev) > 0.7:
        risk_score += 0.2

    if price <= 0:
        risk_score = 1.0

    risk_score = min(1.0, risk_score)

    return {
        "risk_score": round(risk_score, 2),
        "cluster_dev": round(cluster_dev, 2),
        "city_dev": round(city_dev, 2),
        "is_anomaly": risk_score > 0.7
    }
