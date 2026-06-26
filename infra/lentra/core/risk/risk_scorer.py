
def score_risk(listings, market):
    market_price = market.get("market_price") or 0

    for l in listings:
        price = l["normalized_price"]

        deviation = abs(price - market_price) / market_price if market_price else 0

        risk = 0.2
        if deviation > 0.3:
            risk = 0.8
        elif deviation > 0.15:
            risk = 0.5

        l["risk_score"] = round(risk, 2)

    return listings
