from lentra.ux.personalization import load_profile


def score_property(prop, profile=None, features=None):

    score = prop.get("score", 0.5)
    price = prop.get("price", 0)

    # price heuristic
    if price < 400:
        score += 0.3
    elif price < 700:
        score += 0.1
    else:
        score -= 0.2

    # geo boost
    if prop.get("city") in ["Nha Trang", "Da Nang"]:
        score += 0.2

    # personalization layer
    if profile:
        if profile["budget_min"] <= price <= profile["budget_max"]:
            score += 0.4

        if prop.get("city") in profile["preferred_cities"]:
            score += 0.5

    # feature store signals (NO DB ACCESS HERE)
    if features:
        f = features.get(prop.get("id"))

        if f:
            score += f.get("clicks", 0) * 0.05
            score += f.get("likes", 0) * 0.1
            score += f.get("views", 0) * 0.01

    return score


def rank(properties, state=None):

    profile = None
    features = None

    if state and state.get("user_id"):
        profile = load_profile(state["user_id"])

    if state and state.get("feature_store"):
        features = state["feature_store"].load_feedback_agg()

    enriched = []

    for p in properties:
        p["rank_score"] = score_property(p, profile, features)
        enriched.append(p)

    return sorted(enriched, key=lambda x: x["rank_score"], reverse=True)
