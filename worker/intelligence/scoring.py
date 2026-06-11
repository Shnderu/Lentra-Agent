SOURCE_SCORE = {
    "facebook": 0.7,
    "faswaz": 0.9
}

def score_item(item: dict) -> float:
    base = SOURCE_SCORE.get(item.get("source"), 0.5)

    price = item.get("price", 0) or 0

    # простая эвристика: чем дешевле — тем выше score (для аренды)
    price_score = 1 / (1 + price / 1000)

    completeness = 0.5
    if item.get("title"):
        completeness += 0.2
    if item.get("location"):
        completeness += 0.2
    if item.get("url"):
        completeness += 0.1

    return round(base * 0.5 + price_score * 0.3 + completeness * 0.2, 3)
