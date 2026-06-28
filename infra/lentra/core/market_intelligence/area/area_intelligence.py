

def compute_area_intelligence(listing, cluster_stats):

    breakdown = {}
    score = 5.0

    location = (listing.get("location") or "").lower()
    features = listing.get("features") or []

    # 1. Internet quality proxy
    if "internet" in features:
        score += 1.5
        breakdown["internet"] = 1.5
    else:
        score -= 1.0
        breakdown["internet"] = -1.0

    # 2. Beach / location quality
    if "beach" in location or "my khe" in location:
        score += 2.0
        breakdown["beach_access"] = 2.0
    else:
        score -= 0.5
        breakdown["beach_access"] = -0.5

    # 3. Expat density proxy (cluster richness)
    if cluster_stats and cluster_stats.get("listings_count", 0) > 3:
        score += 0.7
        breakdown["expat_density"] = 0.7

    # 4. Infrastructure heuristic
    if "studio" in (listing.get("title") or "").lower():
        score += 0.3
        breakdown["urban_density"] = 0.3

    # clamp
    score = max(0, min(10, score))

    if score >= 8:
        level = "premium"
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
