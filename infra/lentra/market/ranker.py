from lentra.market.scoring import score_property
from lentra.market.dedup import deduplicate

def rank_properties(items: list):
    items = deduplicate(items)

    scored = []

    for item in items:
        item["score"] = score_property(item)
        scored.append(item)

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored
