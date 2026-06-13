# ============================================================
# LISTING DEBUG EXPLAINER V16.8
# ============================================================

def explain_listing(listing: dict):
    return {
        "id": listing.get("id"),
        "price_score": listing.get("price"),
        "trust_score": listing.get("trust_score"),
        "boost": listing.get("personalization_boost"),
        "source": listing.get("source"),
        "why_selected": [
            "passed quality filter",
            "matched geo constraints",
            "ranked by price proximity",
        ],
    }
