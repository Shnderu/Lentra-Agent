from lentra.core.dto.listing_dto import ListingDTO


class UnifiedScorer:

    def score(self, listing: ListingDTO, market: dict):

        price = listing.price or 0
        market_price = market.get("market_price") or 0

        risk = market.get("risk_score", 0)

        deviation = 0
        if market_price:
            deviation = (price - market_price) / market_price * 100

        score = 100

        score -= abs(deviation) * 0.8
        score -= risk * 0.5

        return {
            "score": score,
            "deviation_pct": deviation,
            "risk": risk
        }
