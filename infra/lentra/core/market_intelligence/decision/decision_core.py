from lentra.core.market_intelligence.contracts.market_object_contract import MarketObjectContract


class MarketDecisionCore:

    """
    CONTRACT-LOCKED DECISION LAYER
    """

    def process(self, listing: MarketObjectContract) -> MarketObjectContract:

        # SAFE DEFAULT DECISION (no evaluate anymore)
        listing["verdict"] = "analyzed"

        # deterministic fallback scoring
        risk = listing.get("risk", 0.5)
        price = listing.get("price", 0)

        listing["confidence"] = max(0.3, 1.0 - risk)

        if price > 0:
            listing["attractiveness"] = 1.0 - risk

        return listing
