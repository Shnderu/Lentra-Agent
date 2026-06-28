

from lentra.core.ai.feedback.events.learning_engine import build_preference_weights


def compute_personal_score(listing: dict, profile: dict):

    score = 0

    price = listing["price"]["value"] if isinstance(listing["price"], dict) else listing["price"]

    if price <= profile.get("max_price", 10**9):
        score += 3
    else:
        score -= 2

    # LEARNING SIGNAL (NEW)
    weights = build_preference_weights()

    lid = listing.get("id")

    if lid in weights:
        score += weights[lid]

    return score
