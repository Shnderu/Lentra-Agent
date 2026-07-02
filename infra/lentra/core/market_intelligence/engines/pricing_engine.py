from ._base import BaseEngine


class PricingEngine(BaseEngine):
    def evaluate(self, result, ctx=None):
        if result is None:
            result = {}

        price = result.get("price", 0)
        market = result.get("market_price", 0)

        if market:
            delta = price - market
            score = (price / market) if market else 0
        else:
            delta = 0
            score = 0

        result["pricing"] = {
            "score": score,
            "delta": delta,
            "status": "ok"
        }

        return result
