class PricingEngine:
    def __init__(self):
        pass

    def evaluate(self, price: float, market_price: float):
        if market_price == 0:
            return {"score": 0, "status": "invalid"}

        delta = (price - market_price) / market_price

        return {
            "score": float(1 / (1 + abs(delta))),
            "delta": delta,
            "status": "ok"
        }
