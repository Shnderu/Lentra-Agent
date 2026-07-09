class MarketRankingEngine:
    """
    Market Intelligence ranking engine.

    Unified utility score:
    - pricing value
    - risk
    - area quality
    - confidence
    - duplicate penalty

    Single ranking source of truth.
    """

    def rank(self, cards: list):

        def score(c):

            risk = c.get(
                "risk",
                0.5
            )

            confidence = c.get(
                "confidence",
                0.5
            )

            pricing_score = c.get(
                "pricing_score",
                0.5
            )

            area_score = c.get(
                "area_score",
                0.5
            )

            duplicates = c.get(
                "duplicates",
                0
            )

            #
            # Core intelligence utility
            #

            trust_score = (
                1.0 - risk
            )

            duplicate_penalty = min(
                duplicates * 0.1,
                0.3
            )


            utility = (

                pricing_score * 0.35

                +

                area_score * 0.20

                +

                trust_score * 0.25

                +

                confidence * 0.20

                -

                duplicate_penalty

            )


            return round(
                utility,
                4
            )


        ranked = sorted(
            cards,
            key=score,
            reverse=True
        )


        for index, card in enumerate(
            ranked
        ):

            card["rank"] = index + 1

            card["ranking_score"] = score(
                card
            )


        return ranked
