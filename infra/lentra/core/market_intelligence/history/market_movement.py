from typing import List, Dict, Any


class MarketMovementAnalyzer:
    """
    Market movement intelligence.

    Converts historical price observations
    into market direction signals.
    """


    def analyze(
        self,
        observations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        prices = [
            float(item.get("price"))
            for item in observations
            if item.get("price") is not None
        ]


        if len(prices) < 2:

            return {
                "direction": "unknown",
                "strength": 0,
                "signal": "insufficient_history",
                "samples": len(prices)
            }


        first = prices[0]

        last = prices[-1]


        if first == 0:

            change_percent = 0

        else:

            change_percent = round(
                ((last - first) / first) * 100,
                2
            )


        abs_change = abs(
            change_percent
        )


        if change_percent > 5:

            direction = "up"

            signal = "market_pressure"

        elif change_percent < -5:

            direction = "down"

            signal = "price_decline"

        else:

            direction = "stable"

            signal = "balanced_market"


        strength = min(
            round(
                abs_change / 20,
                2
            ),
            1
        )


        return {

            "direction": direction,

            "strength": strength,

            "signal": signal,

            "change_percent": change_percent,

            "samples": len(prices)

        }
