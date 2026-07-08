from typing import Any


class PropertyRiskEngine:
    """
    MVP Risk Intelligence Engine.

    Evaluates MarketObject risk signals.

    Responsibility:
    - scam probability
    - duplicate risk
    - market anomaly risk
    """


    def evaluate(
        self,
        market_object: Any
    ) -> dict:

        flags = []

        risk_score = 0.0


        duplicate_count = getattr(
            market_object,
            "listing_count",
            0
        )


        confidence = getattr(
            market_object,
            "confidence",
            0.5
        )


        price = getattr(
            market_object,
            "market_price",
            None
        )


        deviation = getattr(
            market_object,
            "price_deviation",
            None
        )


        sources = getattr(
            market_object,
            "sources",
            []
        )


        # duplicate signal

        if duplicate_count >= 3:

            risk_score += 0.35

            flags.append(
                "many_duplicates"
            )

        elif duplicate_count > 1:

            risk_score += 0.15

            flags.append(
                "duplicate_found"
            )


        # confidence signal

        if confidence < 0.5:

            risk_score += 0.3

            flags.append(
                "low_confidence"
            )


        # source signal

        if not sources:

            risk_score += 0.15

            flags.append(
                "unknown_source"
            )


        # price anomaly

        if deviation is not None:

            if abs(deviation) > 0.3:

                risk_score += 0.25

                flags.append(
                    "price_anomaly"
                )


        risk_score = min(
            risk_score,
            1.0
        )


        if risk_score >= 0.7:

            level = "high"

        elif risk_score >= 0.4:

            level = "medium"

        else:

            level = "low"


        return {

            "risk_score": round(
                risk_score,
                3
            ),

            "risk_level": level,

            "flags": flags,

            "confidence": confidence

        }
