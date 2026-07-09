from typing import Dict, Any


class MarketExplanationEngine:
    """
    Converts Market Intelligence signals
    into human readable product explanations.
    """


    def explain(
        self,
        market: Dict[str, Any],
        price_intelligence: Dict[str, Any],
        segment_intelligence: Dict[str, Any],
        market_movement: Dict[str, Any],
    ) -> Dict[str, Any]:

        listing_price = market.get(
            "listing_price",
            0
        )

        market_price = market.get(
            "market_price",
            0
        )

        difference_percent = market.get(
            "difference_percent",
            0
        )


        if difference_percent > 10:

            pricing_explanation = (
                f"Цена выше рынка примерно на "
                f"{difference_percent}%."
            )

            recommendation = "NEGOTIATE"

        elif difference_percent < -10:

            pricing_explanation = (
                f"Цена ниже рынка примерно на "
                f"{abs(difference_percent)}%."
            )

            recommendation = "CHECK"

        else:

            pricing_explanation = (
                "Цена находится в пределах "
                "нормального рыночного диапазона."
            )

            recommendation = "KEEP"



        trend = price_intelligence.get(
            "trend",
            "unknown"
        )

        movement = {
            "increasing":
                "Рынок показывает рост цен.",

            "decreasing":
                "Рынок показывает снижение цен.",

            "stable":
                "Рынок стабилен."
        }.get(
            trend,
            "Недостаточно данных для оценки движения рынка."
        )


        segments = segment_intelligence.get(
            "segments",
            {}
        )


        segment_summary = (
            f"Проанализировано сегментов: "
            f"{len(segments)}."
        )


        return {

            "summary":
                pricing_explanation,

            "pricing_explanation":
                pricing_explanation,

            "segment_explanation":
                segment_summary,

            "movement_explanation":
                movement,

            "recommendation":
                recommendation

        }
