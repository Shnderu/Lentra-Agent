class MarketRankingEngine:
    """
    Market Intelligence ranking engine.

    Uses:
    - pricing intelligence
    - area intelligence
    - risk
    - confidence
    - duplicate signals
    - market snapshot truth

    Single ranking source of truth.
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


            market_score = 0.5


            if market_snapshot:

                median_price = getattr(
                    market_snapshot,
                    "average_market_price",
                    None
                )

                price = c.get(
                    "price",
                    0
                )


                if median_price and price:

                    deviation = abs(
                        price - median_price
                    ) / median_price


                    market_score = max(
                        0,
                        1 - deviation
                    )


            value_score = (

                pricing_score * 0.30

                +

                area_score * 0.20

                +

                confidence * 0.20

                +

                market_score * 0.15

            )


            risk_penalty = (
                risk * 0.35
            )


            duplicate_penalty = min(
                duplicates * 0.05,
                0.2
            )


            price = c.get(
                "price",
                0
            )


            price_penalty = (
                min(
                    price / 1000.0,
                    1.0
                )
                *
                0.1
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
