from .scoring import score_item

def rank(items: list) -> list:
    for item in items:
        item["score"] = score_item(item)

    return sorted(items, key=lambda x: x["score"], reverse=True)
