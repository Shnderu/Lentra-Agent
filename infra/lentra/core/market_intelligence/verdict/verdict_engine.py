class VerdictEngine:

    def evaluate(self, item: dict, market_truth: dict):

        price = item.get("price")
        median = market_truth.get("median_price")

        if not price or not median:
            return "unknown"

        deviation = (price - median) / median

        if deviation < -0.2:
            return "cheap_deal"

        if -0.2 <= deviation <= 0.15:
            return "fair_value"

        if deviation > 0.15:
            return "overpriced"

        return "neutral"
