

def compute_area_score(listing, cluster_stats):

    score = 5.0
    breakdown = {}

    location = (listing.get("location") or "").lower()

    # 1. Beach proximity signal
    if "beach" in location or "my khe" in location:
        score += 2.0
        breakdown["beach_access"] = 2.0
    else:
        score -= 0.5
        breakdown["beach_access"] = -0.5

    # 2. Internet signal
    features = listing.get("features") or []
    if "internet" in features:
        score += 1.5
        breakdown["internet"] = 1.5
    else:
        score -= 1.0
        breakdown["internet"] = -1.0

    # 3. Cluster quality proxy
    if cluster_stats and cluster_stats["avg"] > 500:
        score += 0.5
        breakdown["cluster_quality"] = 0.5

    # clamp 0–10
    score = max(0, min(10, score))

    if score >= 8:
        level = "excellent"
    elif score >= 6:
        level = "good"
    elif score >= 4:
        level = "average"
    else:
        level = "poor"

    return {
        "area_score": round(score, 2),
        "area_level": level,
        "breakdown": breakdown
    }
