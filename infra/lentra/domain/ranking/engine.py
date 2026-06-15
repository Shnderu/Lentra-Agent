from lentra.ux.personalization import load_profile
from lentra.domain.search.text_similarity import text_score
from lentra.domain.search.geo_scoring import geo_score
from lentra.domain.search.intent import detect_intent


def feedback_boost(prop_id, feedback_cache):
    """
    Simple implicit learning signal
    """
    if not feedback_cache:
        return 0.0

    stats = feedback_cache.get(prop_id, {})

    clicks = stats.get("click", 0)
    likes = stats.get("like", 0)
    views = stats.get("view", 0)

    return (clicks * 0.3) + (likes * 0.6) + (views * 0.1)


def score_property(prop, profile=None, query=None, intent=None, user_location=None, feedback_cache=None):
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

    # TEXT
    if query:
        score += text_score(query, prop.get("title", ""))

    # INTENT
    if intent:
        if intent.get("cheap") and price < 400:
            score += 0.5

        if intent.get("luxury") and price > 700:
            score += 0.4

        if intent.get("beach") and prop.get("sea_view"):
            score += 0.5

    # GEO
    score += geo_score(prop, user_location)

    # PERSONALIZATION
    if profile:
        if profile["budget_min"] <= price <= profile["budget_max"]:
            score += 0.4

        if prop.get("city") in profile.get("preferred_cities", []):
            score += 0.5

    # LEARNING LAYER (NEW)
    score += feedback_boost(prop.get("id"), feedback_cache)

    return score


def rank(properties, state=None, query=None, user_location=None, feedback_cache=None):
    profile = None

    if state and state.get("user_id"):
        profile = load_profile(state["user_id"])

    intent = detect_intent(query)

    enriched = []

    for p in properties:
        p["rank_score"] = score_property(
            p,
            profile,
            query,
            intent,
            user_location,
            feedback_cache
        )
        enriched.append(p)

    return sorted(enriched, key=lambda x: x["rank_score"], reverse=True)
