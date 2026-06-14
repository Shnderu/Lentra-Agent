def rank_properties(properties, payload):
    """
    Simple deterministic ranking v1
    """

    budget = payload.get("budget", 10000)
    city = payload.get("city")

    ranked = []

    for p in properties:

        score = 0

        # price score (lower is better)
        if p["price"] <= budget:
            score += 50 + (budget - p["price"]) / 10

        # city match boost
        if city and p["city"] == city:
            score += 30

        # base diversity
        score += 10

        p["rank_score"] = score
        ranked.append(p)

    ranked.sort(key=lambda x: x["rank_score"], reverse=True)

    return ranked
