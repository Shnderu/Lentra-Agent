class PricingEngineAdapter:
    """
    SAFE COMPAT LAYER

    Приводит старый engine (positional args)
    к новому graph contract (dict payload)
    """

    def __init__(self, engine):
        self.engine = engine

    def evaluate(self, payload: dict):
        # SAFE normalize
        price = payload.get("price")
        market_price = payload.get("market_price")

        if price is None or market_price is None:
            return {
                "score": 0,
                "error": "invalid payload"
            }

        # OLD engine compatibility call
        return self.engine.evaluate(price, market_price)
