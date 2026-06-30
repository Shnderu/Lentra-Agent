class ExplanationEngineV1:

    """
    Converts raw scoring into human-readable reasoning
    """

    def explain(self, listing: dict) -> dict:

        risk = listing.get("risk", 0.5)
        price = listing.get("price", 0)
        market = listing.get("market_price", price)

        reasons = []

        if price < market:
            reasons.append("Цена ниже рынка")

        if risk > 0.6:
            reasons.append("высокий риск района")

        if not reasons:
            reasons.append("сбалансированное предложение")

        listing["explanation"] = " • ".join(reasons)

        return listing
