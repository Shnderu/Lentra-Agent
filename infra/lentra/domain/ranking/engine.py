from typing import List, Dict, Any


def rank_properties(properties: List[Dict[str, Any]], query: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Временный стабилизатор ранжирования.
    Без этого API не должен падать.
    """

    if not properties:
        return []

    # минимальный скоринг-заглушка
    def score(p):
        s = 0

        features = query.get("features", {})
        if features.get("pool") and p.get("pool"):
            s += 2
        if features.get("sea_view") and p.get("sea_view"):
            s += 2

        budget_tier = query.get("budget_tier")
        if budget_tier == "low":
            s += 1

        p["_score"] = s
        return s

    return sorted(properties, key=score, reverse=True)
