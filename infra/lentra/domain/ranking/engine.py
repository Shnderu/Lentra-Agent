def score_property(prop, profile=None):
    score = prop.get("score", 0.5)

    price = prop.get("price", 0)

    if price < 400:
        score += 0.3
    elif price < 700:
        score += 0.1
    else:
        score -= 0.2

    if prop.get("city") in ["Nha Trang", "Da Nang"]:
        score += 0.2

    return score


def rank(properties, state=None):
    enriched = []

    for p in properties:
        p["rank_score"] = score_property(p)
        enriched.append(p)

    return sorted(enriched, key=lambda x: x["rank_score"], reverse=True)
