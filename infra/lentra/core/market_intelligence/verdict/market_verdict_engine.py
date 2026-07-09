from typing import Dict, Any


class MarketVerdictEngine:
    """
    Final AI market interpretation layer.

    Converts Market Intelligence signals
    into user facing recommendation.
    """


    def verdict(
        self,
        market: Dict[str, Any],
        price_intelligence: Dict[str, Any],
        market_explanation: Dict[str, Any],
        risk: Dict[str, Any],
        dedup: Dict[str, Any],
        area: Dict[str, Any],
    ) -> Dict[str, Any]:

        score = 0.5

        reasons = []


        difference = market.get(
            "difference_percent",
            0
        )


        if difference > 10:

            score -= 0.15

            reasons.append(
                f"Цена выше рынка на {difference}%."
            )


        elif difference < -10:

            score += 0.15

            reasons.append(
                f"Цена ниже рынка на {abs(difference)}%."
            )


        risk_level = (
            risk.get(
                "risk",
                {}
            )
            .get(
                "level",
                "medium"
            )
        )


        if risk_level == "high":

            score -= 0.2

            reasons.append(
                "Высокий риск объявления."
            )


        duplicates = (
            dedup.get(
                "dedup",
                {}
            )
            .get(
                "duplicates",
                0
            )
        )


        if duplicates > 0:

            reasons.append(
                f"Найдено дублей: {duplicates}."
            )


        movement = price_intelligence.get(
            "trend",
            "unknown"
        )


        if movement == "increasing":

            reasons.append(
                "Рынок показывает рост цен."
            )


        score = max(
            0,
            min(
                score,
                1
            )
        )


        if score >= 0.7:

            action = "GOOD_DEAL"

        elif score <= 0.35:

            action = "NEGOTIATE"

        else:

            action = "REVIEW"



        return {

            "verdict": action,

            "confidence": round(
                score,
                2
            ),

            "reason": " ".join(
                reasons
            ),

            "signals": {

                "price":
                    difference,

                "risk":
                    risk_level,

                "duplicates":
                    duplicates,

                "market_trend":
                    movement

            }

        }
