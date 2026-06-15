from lentra.data.adapter import get_properties
from lentra.domain.ranking.engine import rank


def search_properties(payload, state=None):
    props = get_properties(payload)
    ranked = rank(props, state)

    # normalize output contract (API-safe)
    return [
        {
            "id": p["id"],
            "title": p["title"],
            "price": p["price"],
            "city": p["city"],
            "rank_score": p.get("rank_score", 0)
        }
        for p in ranked
    ]
