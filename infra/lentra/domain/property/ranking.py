from lentra.core.feature_store import feature_store


def rank_property(prop: dict, query: dict) -> float:
    """
    PURE FUNCTION RANKING
    Без DB, без IO, только данные + features.
    """

    features = feature_store.get(prop["id"])

    base_score = prop.get("score", 0.0)
    price = prop.get("price_vnd_mln", 0)

    budget_max = query.get("budget_max")

    # price penalty
    price_penalty = 0.0
    if budget_max and price > budget_max:
        price_penalty = -0.5

    # feature bonus
    feature_bonus = 0.0
    if features.get("sea_view"):
        feature_bonus += 0.2
    if features.get("pool"):
        feature_bonus += 0.1
    if features.get("pet_friendly"):
        feature_bonus += 0.05

    return base_score + price_penalty + feature_bonus
