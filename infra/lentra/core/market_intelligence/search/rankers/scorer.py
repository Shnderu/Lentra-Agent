from typing import List


def score_listing(listing, parsed_query: dict) -> float:
    """
    MVP ranking function.
    Returns higher score = better match.
    """

    score = 0.0

    if not listing:
        return 0.0

    # price relevance
    budget = parsed_query.get("budget")
    if budget:
        try:
            max_price = float(str(budget).replace("$", ""))
            if getattr(listing, "price", 0) <= max_price:
                score += 2.0
            else:
                score -= 1.0
        except Exception:
            pass

    # internet requirement boost
    if parsed_query.get("internet_required"):
        if "wifi" in getattr(listing, "title", "").lower():
            score += 1.0

    # noise sensitivity heuristic
    if parsed_query.get("noise_sensitive"):
        if "quiet" in getattr(listing, "title", "").lower():
            score += 1.0

    return score
