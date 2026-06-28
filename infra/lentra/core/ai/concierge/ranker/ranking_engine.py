

def compute_final_score(listing: dict) -> float:

    price = listing.get("price", 0)
    risk = listing.get("risk", 0.5)
    area = listing.get("area_score", 5)
    meta = listing.get("meta_score", 0.5)

    market = listing.get("market", {})
    deviation = abs(market.get("deviation", 0))

    price_score = max(0, 1 - (price / 1000))

    # market truth penalty (ключевая новая логика)
    market_penalty = deviation * 0.5

    return round(
        meta * 0.35 +
        price_score * 0.2 +
        (1 - risk) * 0.2 +
        (area / 10) * 0.15 -
        market_penalty * 0.1,
        4
    )


def explain_listing(listing: dict, score: float) -> dict:

    reasons = []

    market = listing.get("market", {})
    deviation = market.get("deviation", 0)

    if deviation < -0.1:
        reasons.append("below market price (good deal)")
    elif deviation > 0.1:
        reasons.append("above market price (overpriced)")
    else:
        reasons.append("market aligned")

    if listing.get("risk", 0.5) < 0.6:
        reasons.append("low risk")

    if listing.get("area_score", 5) > 7:
        reasons.append("good area")

    return {
        "score": score,
        "reasons": reasons
    }


def diversity_penalty(item, selected_clusters):

    cluster_id = item["listing"].get("cluster_id")

    if cluster_id in selected_clusters:
        return 0.25

    return 0


def rank_listings(results: list) -> list:

    enriched = []

    for r in results:

        listing = r["listing"]
        score = compute_final_score(listing)

        enriched.append({
            "listing": listing,
            "reason": r.get("reason", ""),
            "final_score": score,
            "explanation": explain_listing(listing, score)
        })

    enriched.sort(key=lambda x: x["final_score"], reverse=True)

    selected_clusters = set()
    final = []

    for item in enriched:

        cluster_id = item["listing"].get("cluster_id")

        item["final_score"] -= diversity_penalty(item, selected_clusters)

        final.append(item)

        if cluster_id:
            selected_clusters.add(cluster_id)

    return sorted(final, key=lambda x: x["final_score"], reverse=True)
