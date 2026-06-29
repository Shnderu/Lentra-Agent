from lentra.core.market_intelligence.object_model.property_object import PropertyObject
from lentra.core.market_intelligence.object_model.mock_data import get_mock_listings


class MarketIntelligenceEngine:

    def analyze(self, property_object):
        if isinstance(property_object, dict):
            query = property_object.get("query", "")
        else:
            query = getattr(property_object, "query", "")

        listings = get_mock_listings(query)

        prices = [l.get("price", 0) for l in listings]

        return {
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "count": len(prices),
            "debug_query": query
        }
