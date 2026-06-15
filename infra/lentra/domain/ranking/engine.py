from typing import List, Dict, Any


def rank_properties(properties: List[Dict[str, Any]], query: Dict[str, Any]) -> List[Dict[str, Any]]:

    raw = query.get("raw", "").lower()
    features = query.get("features", {})

    scored = []

    for p in properties:
        score = 0.0

        # CITY MATCH
        if "da nang" in raw and "da nang" in (p.get("city") or "").lower():
            score += 2.0

        # SEA VIEW MATCH
        if features.get("sea_view") and p.get("sea_view"):
            score += 2.0

        # POOL MATCH
        if features.get("pool") and p.get("pool"):
            score += 3.0

        # PET MATCH
        if features.get("pet_friendly") and p.get("pet_friendly"):
            score += 1.0

        # PRICE heuristic (cheap bias)
        if "cheap" in raw and p.get("price_vnd_mln", 999) < 20:
            score += 1.5

        p["score"] = score
        scored.append(p)

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored
