class MarketTruthEngineV1:
    """
    Computes true market baseline from clustered data.
    """

    def compute_truth(self, cards: list):

        prices = [c.get("price") or 0 for c in cards]

        if not prices:
            return {
                "market_truth": 0,
                "volatility": 0
            }

        prices_sorted = sorted(prices)
        median = prices_sorted[len(prices_sorted) // 2]

        spread = max(prices) - min(prices) if prices else 0
        volatility = spread / (median + 1)

        return {
            "market_truth": median,
            "volatility": volatility
        }
