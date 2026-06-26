from typing import List, Dict, Any


class MarketIntelligenceV2:

    def build_market_context(self, listings: List[Dict[str, Any]], query: Dict[str, Any]) -> Dict[str, Any]:
        """
        v2: расширенный market layer (город, тип, бюджет)
        """

        prices = [x.get("price") for x in listings if x.get("price")]

        if not prices:
            return {
                "market_price": None,
                "bands": {},
                "note": "no data"
            }

        avg = sum(prices) / len(prices)

        return {
            "market_price": round(avg, 2),
            "min": min(prices),
            "max": max(prices),
            "bands": {
                "cheap": avg * 0.8,
                "market": avg,
                "expensive": avg * 1.2
            },
            "city": query.get("city"),
            "type": query.get("type"),
            "budget": query.get("budget")
        }
