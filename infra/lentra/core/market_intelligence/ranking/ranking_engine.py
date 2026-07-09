class MarketRankingEngine:
    """
    Market Intelligence ranking engine v2.

    Ranking principles:

    - Risk protects user from bad objects.
    - Market opportunity increases value.
    - Ranking selects best market opportunities.

    Signals:
    - pricing intelligence
    - market deviation
    - area quality
    - confidence
    - risk
    - duplicates
    """


    def rank(
        self,
        cards: list,
        market_snapshot=None
    ):


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


            price = c.get(
                "price",
                0
            )


            market_price = c.get(
                "market_price",
                None
            )


            market_score = 0.5

            opportunity_bonus = 0.0


            # =========================
            # MARKET OPPORTUNITY
            # =========================

            if market_price and price:

                deviation = (
                    market_price - price
                ) / market_price


                if deviation > 0:

                    opportunity_bonus = min(
                        deviation * 0.35,
                        0.20
                    )


                market_score = max(
                    0,
                    min(
                        1,
                        1 - abs(deviation)
                    )
                )


            value_score = (

                pricing_score * 0.25

                +

                area_score * 0.20

                +

                confidence * 0.20

                +

                market_score * 0.15

                +

                opportunity_bonus

            )


            risk_penalty = (
                risk * 0.35
            )


            duplicate_penalty = min(
                duplicates * 0.05,
                0.2
            )


            price_penalty = (
                min(
                    price / 1000.0,
                    1.0
                )
                *
                0.05
            )


            return round(

                value_score

                -

                risk_penalty

                -

                duplicate_penalty

                -

                price_penalty,

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
