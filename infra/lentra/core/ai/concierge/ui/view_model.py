

def build_listing_card(listing: dict) -> dict:

    market = listing.get("market", {})
    negotiation = listing.get("negotiation", {})
    persona = listing.get("persona", {})

    return {
        "id": listing.get("id"),

        # --- core info ---
        "price": listing.get("price"),
        "market_price": market.get("market_avg"),
        "price_deviation": market.get("deviation"),
        "verdict": market.get("verdict"),

        # --- risk ---
        "risk": listing.get("risk"),
        "risk_level": "high" if listing.get("risk", 0) > 0.7 else "medium",

        # --- area ---
        "area_score": listing.get("area_score"),

        # --- ranking ---
        "score": listing.get("meta_score"),

        # --- negotiation ---
        "negotiation": {
            "strategy": negotiation.get("strategy"),
            "target_price": negotiation.get("target_price"),
            "discount_potential": negotiation.get("discount_potential")
        },

        # --- AI assistant layer ---
        "ai": {
            "verdict": persona.get("verdict"),
            "advice": persona.get("advice"),
            "warnings": persona.get("warnings")
        },

        # --- UI hints ---
        "ui_badges": generate_badges(listing)
    }


def generate_badges(listing: dict) -> list:

    badges = []

    market = listing.get("market", {})
    risk = listing.get("risk", 0.5)

    if market.get("verdict") == "undervalued":
        badges.append("🔥 Good Deal")

    if risk > 0.7:
        badges.append("⚠ High Risk")

    if listing.get("area_score", 0) > 7:
        badges.append("📍 Prime Area")

    if listing.get("meta_score", 0) > 0.6:
        badges.append("⭐ Top Match")

    return badges
