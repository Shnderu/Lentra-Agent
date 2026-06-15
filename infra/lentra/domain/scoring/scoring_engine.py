def score_properties(properties, query_obj):
    results = []

    for p in properties:
        score = 0.0

        # Базовый скор по цене (дешевле = лучше)
        if p.get("price_vnd_mln"):
            score += max(0, 1 - p["price_vnd_mln"] / 50)

        # pool preference
        if query_obj.pool and p.get("pool"):
            score += 0.3

        # sea view preference
        if query_obj.sea_view and p.get("sea_view"):
            score += 0.2

        # city match
        if query_obj.city and p.get("city") == query_obj.city:
            score += 0.2

        p["score"] = round(score, 3)
        results.append(p)

    return results
