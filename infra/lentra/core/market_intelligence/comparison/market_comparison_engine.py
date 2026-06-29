class MarketComparisonEngine:
    """
    Compares listings against each other inside same request batch.
    Produces relative ranking signals.
    """

    def compare(self, cards: list):

        if not cards:
            return cards

        # -------------------------
        # BASELINE METRICS
        # -------------------------
        avg_price = sum(c.get("price") or 0 for c in cards) / len(cards)

        avg_confidence = sum(c.get("confidence") or 0 for c in cards) / len(cards)

        # -------------------------
        # RELATIVE SCORING
        # -------------------------
        for card in cards:

            price = card.get("price") or 0

            # relative position vs batch
            relative_price = (price - avg_price) / (avg_price + 1e-6)

            # competitiveness score
            card["comparison"] = {
                "relative_price": round(relative_price, 4),
                "price_vs_market_batch": round(price - avg_price, 2),
                "confidence_vs_batch": round((card.get("confidence") or 0) - avg_confidence, 4)
            }

            # ranking hint
            if relative_price < -0.15:
                card["labels"].append("best_value")
            elif relative_price > 0.15:
                card["labels"].append("premium_listing")

        return cards
