from lentra.core.market_intelligence.pricing.market_truth_engine import MarketTruthEngine


class RiskEngine:

    def __init__(self):
        self.market = MarketTruthEngine()

    def evaluate(self, listing: dict):

        # register listing into market memory
        self.market.update(listing)

        def safe(v):
            if v is None:
                return 0.5
            try:
                return float(v)
            except Exception:
                return 0.5

        price = safe(listing.get("price"))
        deviation = self.market.price_deviation(listing)

        risk = 0.5

        # -------------------------
        # MARKET-BASED RISK (NEW CORE SIGNAL)
        # -------------------------
        if deviation > 0.25:
            risk += 0.25

        if deviation < -0.25:
            risk += 0.10  # underpriced can also be suspicious

        # -------------------------
        # HEURISTICS (EXISTING)
        # -------------------------
        if price < 150:
            risk += 0.1

        if not listing.get("photos"):
            risk += 0.1

        if "urgent" in (listing.get("title") or "").lower():
            risk += 0.1

        # clamp
        risk = max(0.0, min(1.0, risk))

        return {
            "risk": risk,
            "price_deviation": deviation
        }
