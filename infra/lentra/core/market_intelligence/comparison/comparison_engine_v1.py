class ComparisonEngineV1:
    """
    v1 comparison layer:
    - compares listings inside same response
    - computes relative market position
    - marks best/worst opportunities
    """

    def compare(self, cards: list):

        if not cards:
            return cards

        # -------------------------
        # BASE STATISTICS
        # -------------------------
        prices = [c.get("price") or 0 for c in cards]
        risks = [c.get("risk") or 0.5 for c in cards]
        confs = [c.get("confidence") or 0.5 for c in cards]

        median_price = sorted(prices)[len(prices) // 2]

        # -------------------------
        # ENRICH EACH CARD
        # -------------------------
        for c in cards:

            price = c.get("price") or 0

            # relative price position
            if median_price > 0:
                c["price_vs_market"] = (price - median_price) / median_price * 100
            else:
                c["price_vs_market"] = 0.0

            # risk-adjusted attractiveness
            c["attractiveness"] = (c.get("confidence", 0.5) * (1 - c.get("risk", 0.5)))

            # comparison labels
            labels = c.get("labels", [])

            if price < median_price:
                labels.append("below_market")
            elif price > median_price:
                labels.append("above_market")
            else:
                labels.append("market_equal")

            if c.get("risk", 0.5) > 0.7:
                labels.append("high_risk")

            c["labels"] = list(set(labels))

        # -------------------------
        # RANK WITHIN COMPARISON CONTEXT
        # -------------------------
        cards.sort(key=lambda x: x.get("attractiveness", 0), reverse=True)

        for i, c in enumerate(cards):
            c["comparison_rank"] = i + 1

        # -------------------------
        # BEST / WORST FLAGS
        # -------------------------
        if cards:
            cards[0]["is_best_deal"] = True
            cards[-1]["is_worst_deal"] = True

        return cards
