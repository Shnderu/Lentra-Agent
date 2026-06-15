from typing import List, Dict


def rank_properties(properties: List[Dict], query: Dict) -> List[Dict]:
    """
    PURE RANKING FUNCTION (NO IO)

    MVP scoring model:
    - price penalty
    - random baseline boost (placeholder)
    """

    max_budget = query.get("budget_max", 10**9)

    scored = []

    for p in properties:
        price = p.get("price") or 0

        # budget filter (soft)
        budget_score = 1.0 if price <= max_budget else 0.3

        # simple heuristic score
        score = budget_score

        scored.append({
            **p,
            "rank_score": round(score, 3)
        })

    scored.sort(key=lambda x: x["rank_score"], reverse=True)

    return scored
