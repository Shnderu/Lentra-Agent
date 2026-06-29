class RankingEngine:

    def score(self, listing: dict, context: dict = None) -> float:

        base = 0.5

        risk = listing.get("risk", 0.5)
        if risk is None:
            risk = 0.5

        area = listing.get("area_score", 5.0)
        if area is None:
            area = 5.0

        price_deviation = listing.get("price_deviation", 0.0)
        if price_deviation is None:
            price_deviation = 0.0

        # risk penalty
        base -= float(risk) * 0.4

        # area bonus/penalty
        base += (float(area) - 5.0) * 0.05

        # price deviation penalty
        base -= abs(float(price_deviation)) * 0.3

        # clamp
        if base < 0:
            base = 0.0
        if base > 1:
            base = 1.0

        return base
