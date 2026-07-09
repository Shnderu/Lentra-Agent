from typing import List, Dict, Any


class PriceTrendAnalyzer:
    """
    Product level price intelligence.

    Converts raw price history into market signals.
    """

    def analyze(
        self,
        prices: List[float]
    ) -> Dict[str, Any]:

        if not prices:
            return {
                "trend": "unknown",
                "signal": "no_history",
                "change_percent": 0
            }


        if len(prices) == 1:
            return {
                "trend": "stable",
                "signal": "initial_observation",
                "change_percent": 0
            }


        first = prices[0]
        last = prices[-1]


        if first == 0:
            change = 0
        else:
            change = round(
                ((last - first) / first) * 100,
                2
            )


        if change < -5:
            trend = "decreasing"
            signal = "seller_reduced_price"

        elif change > 5:
            trend = "increasing"
            signal = "market_pressure"

        else:
            trend = "stable"
            signal = "normal_listing"


        return {

            "trend": trend,

            "signal": signal,

            "change_percent": change,

            "history": prices

        }
