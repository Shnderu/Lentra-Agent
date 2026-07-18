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
        combine market + segment context
    """


    def verdict(
        self,
        market: Dict[str, Any],
        price_intelligence: Dict[str, Any],
        market_explanation: Dict[str, Any],
        risk: Dict[str, Any],
        dedup: Dict[str, Any],
        area: Dict[str, Any],
        segment_signal: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        reasons = []

        segment_signal = (
            segment_signal
            if isinstance(segment_signal, dict)
            else {}
        )


        difference = market.get(
            "difference_percent",
            0
        )


        if difference < -10:

            reasons.append(
                f"Цена ниже общего рынка на {abs(difference)}%."
            )


        elif difference > 10:

            reasons.append(
                f"Цена выше общего рынка на {difference}%."
            )


        else:

            reasons.append(
                "Цена находится в пределах общего рыночного диапазона."
            )


        segment_position = segment_signal.get(
            "position",
            "unknown"
        )

        segment_delta = segment_signal.get(
            "segment_price_delta_percent",
            0
        )


        if segment_position == "below_segment_market":

            reasons.append(
                f"Объект дешевле своего сегмента на {abs(segment_delta)}%."
            )


        elif segment_position == "above_segment_market":

            reasons.append(
                f"Объект дороже своего сегмента на {segment_delta}%."
            )


        segment_status = segment_signal.get(
            "status",
            "unknown"
        )


        if segment_status == "premium":

            if segment_position == "within_segment_market":

                reasons.append(
                    "Цена соответствует уровню своего сегмента."
                )

            reasons.append(
                "Объект находится в премиальном сегменте района."
            )


        elif segment_status == "insufficient_data":

            reasons.append(
                "Сегмент недостаточно подтвержден рыночными данными."
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
                    trend,

                "segment":
                    segment_signal

            }

        }
