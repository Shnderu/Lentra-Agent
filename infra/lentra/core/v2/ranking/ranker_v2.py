from typing import List, Dict, Any


class RankerV2:

    def rank(self, listings: List[Dict[str, Any]], market_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        v2 ranking:
        - deviation from market
        - risk penalty
        - price attractiveness
        """

        market_price = market_context.get("market_price")

        def score(item: Dict[str, Any]) -> float:
            base = 100

            price = item.get("price", 0)
            risk = item.get("risk_score", 0)

            # price signal
            if market_price and price:
                deviation = abs(price - market_price) / market_price * 100
                base -= deviation * 0.8

            # risk penalty
            base -= risk * 1.2

            # bonus for cheap good deals
            if market_price and price and price < market_price * 0.9:
                base += 10

            return base

        return sorted(listings, key=score, reverse=True)
