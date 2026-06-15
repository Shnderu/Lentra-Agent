from lentra.ux.personalization import load_profile
from lentra.domain.search.text_similarity import text_score


def score_property(prop, profile=None, query=None):
    score = prop.get("score", 0.5)

    price = prop.get("price", 0) or 0

    # PRICE MODEL
    if price < 400:
        score += 0.3
    elif price < 700:
        score += 0.1
    else:
        score -= 0.2

    # CITY BOOST
    if prop.get("city") in ["Nha Trang", "Da Nang"]:
        score += 0.2

    # TEXT RELEVANCE BOOST (NEW)
    if query:
        score += text_score(query, prop.get("title", ""))

    # PERSONALIZATION
    if profile:
        if profile["budget_min"] <= price <= profile["budget_max"]:
            score += 0.4

        if prop.get("city") in profile.get("preferred_cities", []):
            score += 0.5

    return score


def rank(properties, state=None, query=None):
    profile = None

    if state and state.get("user_id"):
        profile = load_profile(state["user_id"])

    enriched = []

    for p in properties:
        p["rank_score"] = score_property(p, profile, query)
        enriched.append(p)

    return sorted(enriched, key=lambda x: x["rank_score"], reverse=True)
