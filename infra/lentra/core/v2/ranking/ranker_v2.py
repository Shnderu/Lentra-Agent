from typing import List, Dict, Any
from lentra.core.v2.models.listing import Listing


class RankerV2:
    """
    V2 ranking engine:
    - market deviation aware ranking
    - risk-aware weighting
    - fully Listing-based (no dict access)
    """

    def rank(self, listings: List[Listing], market: Dict[str, Any]) -> List[Listing]:

        market_price = market.get("market_price") if market else None

        for listing in listings:

            score = 0

            price = listing.price or 0
            risk = listing.risk_score or 0

            # -----------------------------
            # Market deviation scoring
            # -----------------------------
            if market_price and price:
                deviation = abs(price - market_price) / market_price * 100
                listing.market_deviation = deviation

                # sweet spot: near market price
                if deviation < 10:
                    score += 30
                elif deviation < 25:
                    score += 15
                else:
                    score -= 10

            # -----------------------------
            # Risk penalty
            # -----------------------------
            score -= risk * 0.5

            # -----------------------------
            # Duplicate penalty
            # -----------------------------
            if listing.duplicates:
                score -= len(listing.duplicates) * 5

            listing.ranking_score = score

        # final sort
        listings.sort(key=lambda x: x.ranking_score, reverse=True)

        return listings


# backward compatibility
def rank_listings_v2(listings: List[Listing], market: Dict[str, Any]):
    return RankerV2().rank(listings, market)
