from typing import List, Dict, Any


class MarketRegimeEngine:

    def detect(self, history: List[List[Dict[str, Any]]]) -> Dict[str, Any]:

        if len(history) < 3:
            return {
                "regime": "unknown",
                "volatility": 0.0,
                "trend": "flat"
            }

        last = history[-1]
        prev = history[-2]
        prev2 = history[-3]

        def get(sig_list, name):
            for s in sig_list:
                if s.get("name") == name:
                    return s.get("value")
            return None

        prices = [
            get(prev2, "price"),
            get(prev, "price"),
            get(last, "price"),
        ]

        prices = [p for p in prices if p is not None]

        if len(prices) < 3:
            return {
                "regime": "insufficient_data",
                "volatility": 0.0,
                "trend": "flat"
            }

        # -------------------------
        # VOLATILITY
        # -------------------------
        changes = [
            abs(prices[i] - prices[i - 1]) / max(prices[i - 1], 1)
            for i in range(1, len(prices))
        ]

        volatility = sum(changes) / len(changes)

        # -------------------------
        # TREND
        # -------------------------
        if prices[-1] > prices[0] * 1.05:
            trend = "uptrend"
        elif prices[-1] < prices[0] * 0.95:
            trend = "downtrend"
        else:
            trend = "flat"

        # -------------------------
        # REGIME CLASSIFICATION
        # -------------------------
        if volatility > 0.1:
            regime = "volatile"
        elif trend == "uptrend":
            regime = "bull"
        elif trend == "downtrend":
            regime = "bear"
        else:
            regime = "stable"

        return {
            "regime": regime,
            "volatility": round(volatility, 4),
            "trend": trend
        }
