def score_property(item: dict, query: dict = None):
    score = 0.0

    price = item.get("price", 0)
    district = item.get("district", "")

    # PRICE SCORE (main factor)
    if price < 400:
        score += 0.5
    elif price < 600:
        score += 0.3
    else:
        score += 0.1

    # LOCATION SCORE
    if district in ["D1", "D2"]:
        score += 0.3
    else:
        score += 0.1

    # TITLE QUALITY (heuristic)
    if "studio" in item.get("title", "").lower():
        score += 0.1

    return round(score, 3)
