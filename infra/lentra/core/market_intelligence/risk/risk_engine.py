class RiskEngine:

    def evaluate(self, listing: dict):

        def safe(v):
            if v is None:
                return 0.5
            try:
                return float(v)
            except Exception:
                return 0.5

        risk = 0.5

        price = safe(listing.get("price"))
        deviation = safe(listing.get("price_deviation"))

        # market-driven risk
        if deviation > 0.25:
            risk += 0.25

        if price < 150:
            risk += 0.1

        if not listing.get("photos"):
            risk += 0.1

        if "urgent" in (listing.get("title") or "").lower():
            risk += 0.1

        risk = max(0.0, min(1.0, risk))

        return {
            "risk": risk
        }
