

class MarketIntelligenceEngine:

    def analyze(self, property_object):

        prices = [l.get("price", 0) for l in property_object.listings]

        if not prices:
            return {
                "market_price": 0,
                "deviation": 0,
                "verdict": "unknown",
                "risk": 0.5
            }

        market_price = sum(prices) / len(prices)

        # baseline deviation logic
        deviation = max(prices) - min(prices) if len(prices) > 1 else 0

        avg_price = market_price

        listing_price = prices[0]

        price_diff = (listing_price - avg_price) / (avg_price + 1e-8)

        # verdict logic
        if price_diff < -0.15:
            verdict = "underpriced"
            risk = 0.7
        elif price_diff > 0.25:
            verdict = "overpriced"
            risk = 0.8
        else:
            verdict = "market_aligned"
            risk = 0.4

        return {
            "market_price": avg_price,
            "price_deviation": price_diff,
            "price_spread": deviation,
            "verdict": verdict,
            "risk": risk
        }
