from .base import EngineV3

class RiskEngine(EngineV3):
    name = "risk"

    def evaluate(self, context: dict, result: dict):
        price = context.get("price", 0)
        market_price = context.get("market_price", 1)

        delta = abs(price - market_price) / max(market_price, 1)

        result["risk"] = {
            "delta": delta,
            "level": "low" if delta < 0.2 else "high"
        }

        return result
