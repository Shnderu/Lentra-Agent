from typing import Dict, Any


class SegmentExplanationEngine:
    """
    Segment market explanation layer.

    Converts existing segment market signals
    into user-facing intelligence.

    Does NOT calculate market truth.
    Uses MarketTruthEngine output.
    """


    def explain(
        self,
        segment_market: Dict[str, Any],
        segment_signal: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        segment_signal = segment_signal or {}

        if not isinstance(
            segment_market,
            dict
        ):
            segment_market = {}


        sample_size = segment_market.get(
            "sample_size",
            0
        )


        median_price = segment_market.get(
            "median_price"
        )


        confidence = segment_signal.get(
            "confidence",
            0
        )


        if sample_size == 0:

            status = "unknown"

            message = (
                "Недостаточно данных "
                "для оценки сегмента."
            )


        elif sample_size == 1:

            status = "limited"

            message = (
                "Найден один похожий объект. "
                "Оценка сегмента предварительная."
            )


        elif sample_size < 5:

            status = "limited"

            message = (
                "Сегмент имеет несколько наблюдений. "
                "Рыночная оценка ограниченной точности."
            )


        else:

            status = "stable"

            message = (
                "Сегмент имеет достаточную историю. "
                "Рыночная оценка стабильна."
            )


        return {

            "status": status,

            "message": message,

            "sample_size": sample_size,

            "median_price": median_price,

            "confidence": confidence

        }
