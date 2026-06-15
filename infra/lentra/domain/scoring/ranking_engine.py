from lentra.domain.scoring.weights import WEIGHTS
from lentra.domain.scoring.normalizer import normalize_price


def rank_properties(properties, query_obj):
    results = []

    for p in properties:
        breakdown = {}

        # PRICE
        price_score = normalize_price(p.get("price_vnd_mln", 0))
        breakdown["price"] = price_score * WEIGHTS["price"]

        # POOL
        pool_score = 1.0 if query_obj.pool and p.get("pool") else 0.0
        breakdown["pool"] = pool_score * WEIGHTS["pool"]

        # SEA VIEW
        sea_score = 1.0 if query_obj.sea_view and p.get("sea_view") else 0.0
        breakdown["sea_view"] = sea_score * WEIGHTS["sea_view"]

        # CITY
        city_score = 1.0 if query_obj.city and p.get("city") == query_obj.city else 0.0
        breakdown["city"] = city_score * WEIGHTS["city"]

        total = sum(breakdown.values())

        results.append({
            **p,
            "score": round(total, 4),
            "score_breakdown": breakdown
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
