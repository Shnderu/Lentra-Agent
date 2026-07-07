from typing import Dict, Any


class RiskEngine:
    """
    Market Intelligence Risk Engine v1.

    Responsibility:
    - estimate anomaly risk
    - separate price opportunity from fraud suspicion
    - enrich object with risk intelligence

    Rule:
    low price != fraud
    """

    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        price = float(
            result.get(
                "price",
                0
            )
        )

        market = float(
            result.get(
                "market_price",
                0
            )
        )

        source = result.get(
            "source",
            "unknown"
        )

        if market > 0:
            deviation = (
                price - market
            ) / market
        else:
            deviation = 0.0


        absolute_deviation = abs(
            deviation
        )


        # ---------------------------------
        # Price anomaly
        # ---------------------------------

        if absolute_deviation <= 0.15:
            price_signal = "normal"

        elif deviation < 0:
            price_signal = "below_market"

        else:
            price_signal = "above_market"


        # ---------------------------------
        # Fraud probability
        # ---------------------------------

        fraud_score = 0.1


        # Extremely cheap offers require review
        if deviation <= -0.40:
            fraud_score += 0.45

        elif deviation <= -0.25:
            fraud_score += 0.25


        # Unknown source penalty
        if source == "unknown":
            fraud_score += 0.1


        fraud_score = min(
            fraud_score,
            1.0
        )


        if fraud_score >= 0.7:
            level = "high"

        elif fraud_score >= 0.35:
            level = "medium"

        else:
            level = "low"


        result["risk"] = {
            "fraud_score": round(
                fraud_score,
                4
            ),

            "level": level,

            "price_signal": price_signal,

            "deviation": round(
                deviation,
                4
            ),

            "source": source,

            "status": "ok"
        }


        return result
