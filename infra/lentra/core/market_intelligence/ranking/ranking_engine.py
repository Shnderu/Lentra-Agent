class MarketRankingEngine:
    """
    Market Intelligence ranking engine.

    Ranks listings by real market utility:

    - pricing value
    - risk quality
    - area quality
    - data confidence
    - duplicate penalty

    This engine does not make final decisions.
    Decision Layer remains responsible for ACCEPT/REVIEW/REJECT.
    """

    def rank(
        self,
        cards: list
    ):

        def score(card):

            pricing_score = card.get(
                "pricing_score",
                0.5
            )

            area_score = card.get(
                "area_score",
                0.5
            )

            confidence = card.get(
                "confidence",
                0.5
            )

            risk = card.get(
                "risk",
                0.5
            )

            duplicates = card.get(
                "duplicates",
                0
            )


            risk_quality = 1 - risk


            duplicate_penalty = min(
                duplicates * 0.05,
                0.15
            )


            utility = (

                pricing_score * 0.35

                +

                risk_quality * 0.25

                +

                area_score * 0.20

                +

                confidence * 0.15

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
