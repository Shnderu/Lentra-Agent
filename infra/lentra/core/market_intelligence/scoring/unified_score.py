from lentra.core.market_intelligence.models.market_object import MarketObject


class UnifiedScoreEngine:
    """
    Unified Market Intelligence score.

    Combines:
        - Pricing Intelligence
        - Property Risk
        - Area Intelligence

    Produces a single normalized score that can later
    be consumed by the AI Decision Layer.
    """

    def compute(
        self,
        obj: MarketObject
    ) -> MarketObject:

        market_price = obj.market_price or 0.0

        if market_price:

            price = (
                obj.listings[0].price
                if obj.listings
                else market_price
            )

            deviation = (
                price - market_price
            ) / market_price

        else:

            deviation = 0.0

        price_signal = max(
            -1.0,
            min(
                1.0,
                -deviation
            )
        )

        area_signal = (
            (obj.area_score - 5.0)
            / 5.0
        )

        risk_signal = (
            0.5 - obj.risk
        )

        final_score = (

            price_signal * 0.50 +

            area_signal * 0.35 +

            risk_signal * 0.15

        )

        final_score = max(
            -1.0,
            min(
                1.0,
                final_score
            )
        )

        if final_score >= 0.30:

            verdict = "good_deal"

        elif final_score <= -0.30:

            verdict = "overpriced"

        else:

            verdict = "fair"

        confidence = max(
            0.0,
            min(
                1.0,
                (
                    obj.confidence * 0.50
                    +
                    (1.0 - obj.risk) * 0.30
                    +
                    (obj.area_score / 10.0) * 0.20
                )
            )
        )

        obj.price_deviation = round(
            deviation,
            4
        )

        obj.confidence = round(
            confidence,
            4
        )

        obj.verdict = verdict

        if obj.negotiation is None:
            obj.negotiation = {}

        obj.negotiation["market_score"] = round(
            final_score,
            4
        )

        return obj
