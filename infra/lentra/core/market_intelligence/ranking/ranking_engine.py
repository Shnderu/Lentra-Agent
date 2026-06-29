class MarketRankingEngine:
    """
    Ranks listings using composite utility function:
    value vs price vs risk vs confidence.
    """

    def rank(self, cards: list):

        def score(c):

            price = c.get("price") or 0
            risk = c.get("risk") or 0.5
            confidence = c.get("confidence") or 0.5

            # normalized utility model
            value_score = confidence * (1.0 - risk)

            # penalize expensive listings slightly
            price_penalty = min(price / 1000.0, 1.0) * 0.2

            return value_score - price_penalty

        ranked = sorted(cards, key=score, reverse=True)

        # attach rank
        for i, c in enumerate(ranked):
            c["rank"] = i + 1

        return ranked
