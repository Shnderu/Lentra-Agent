from lentra.domain.user.profile import get_profile


def score_property(user_id: int, prop: dict):

    profile = get_profile(user_id)

    score = 0.0

    # 1. бюджет
    budget = profile.get("budget_pref", 500)

    if prop["price"] <= budget:
        score += 0.5
    else:
        score -= 0.3

    # 2. город
    city_pref = profile.get("cities", {})

    city_weight = city_pref.get(prop["city"], 0.2)
    score += city_weight

    # 3. базовая нормализация
    score += prop.get("rank_score", 0)

    return round(score, 3)


def rank_properties(user_id: int, properties: list):

    for p in properties:
        p["score"] = score_property(user_id, p)

    return sorted(properties, key=lambda x: x["score"], reverse=True)
