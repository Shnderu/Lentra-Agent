

def build_concierge_response(listing: dict) -> dict:

    price = listing.get("price", 0)
    risk = listing.get("risk", 0.5)
    market = listing.get("market", {})
    negotiation = listing.get("negotiation", {})

    advice = []
    warnings = []

    # --- decision logic ---
    if risk > 0.7:
        warnings.append("High fraud probability — verify landlord identity")

    if market.get("verdict") == "overpriced":
        advice.append("Try negotiation before committing")

    if negotiation.get("strategy") == "aggressive_negotiation":
        advice.append(
            f"Start offer at ~{negotiation.get('target_price')} USD"
        )

    if price < market.get("market_avg", price):
        advice.append("This is a below-market opportunity — act fast")

    # --- final verdict ---
    if risk < 0.5 and market.get("verdict") == "market aligned":
        verdict = "safe_deal"
    elif risk > 0.7:
        verdict = "high_risk"
    else:
        verdict = "neutral_deal"

    return {
        "verdict": verdict,
        "advice": advice,
        "warnings": warnings,
        "summary": "AI concierge recommendation generated"
    }
