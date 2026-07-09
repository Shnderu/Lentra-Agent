from typing import Dict, Any


class MarketVerdictEngine:
    """
    Market interpretation layer.

    IMPORTANT:
    This module does NOT make final decisions.

    Final decision authority:
        DecisionLayer

    Responsibility:
        explain market situation
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

        reasons = []


        difference = market.get(
            "difference_percent",
            0
        )


        if difference < -10:

            reasons.append(
                f"Цена ниже рынка на {abs(difference)}%."
            )


        elif difference > 10:

            reasons.append(
                f"Цена выше рынка на {difference}%."
            )


        else:

            reasons.append(
                "Цена находится в пределах рыночного диапазона."
            )


        risk_level = (
            risk.get(
                "risk",
                {}
            )
            .get(
                "level",
                "unknown"
            )
        )


        reasons.append(
            f"Риск объявления: {risk_level}."
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


        if duplicates:

            reasons.append(
                f"Найдено дублей: {duplicates}."
            )


        trend = price_intelligence.get(
            "trend",
            "unknown"
        )


        if trend != "unknown":

            reasons.append(
                f"Рыночный тренд: {trend}."
            )


        return {

            "verdict": "MARKET_ANALYSIS",

            "confidence": round(
                market.get(
                    "confidence",
                    0.5
                ),
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
                    trend

            }

        }
