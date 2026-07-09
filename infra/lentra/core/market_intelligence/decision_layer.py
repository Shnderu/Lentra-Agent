from lentra.core.market_intelligence.models.market_object import MarketObject


class DecisionLayer:
    """
    Final Market Intelligence decision layer.

    Consumes MarketObject enriched by:
        - Pricing
        - Risk
        - Area
        - Unified Score

    Produces a user-facing recommendation.
    """

    def evaluate(
        self,
        obj: MarketObject
    ) -> dict:

        market_score = obj.negotiation.get(
            "market_score",
            0.0
        )

        if (
            market_score >= 0.50
            and obj.risk <= 0.30
        ):

            decision = "buy"

        elif (
            market_score >= 0.15
            and obj.risk <= 0.50
        ):

            decision = "negotiate"

        else:

            decision = "skip"

        explanation = []

        if obj.price_deviation is not None:

            if obj.price_deviation > 0.10:

                explanation.append(
                    "price_above_market"
                )

            elif obj.price_deviation < -0.10:

                explanation.append(
                    "price_below_market"
                )

        if obj.area_score >= 7:

            explanation.append(
                "good_area"
            )

        if obj.risk <= 0.30:

            explanation.append(
                "low_risk"
            )

        elif obj.risk >= 0.70:

            explanation.append(
                "high_risk"
            )

        return {
            "decision": decision,
            "market_score": round(
                market_score,
                4
            ),
            "confidence": round(
                obj.confidence,
                4
            ),
            "verdict": obj.verdict,
            "risk": round(
                obj.risk,
                4
            ),
            "area_score": round(
                obj.area_score,
                2
            ),
            "price_deviation": obj.price_deviation,
            "reasons": explanation,
        }
