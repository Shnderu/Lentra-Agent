from typing import Dict, Any


class PricingAdapter:

    def __init__(self, pricing_engine):
        self.engine = pricing_engine

    def get_market_price(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        # normalize call across possible implementations
        if hasattr(self.engine, "analyze"):
            res = self.engine.analyze(payload)
            if isinstance(res, dict):
                return res
            if hasattr(res, "to_dict"):
                return res.to_dict()

        if hasattr(self.engine, "get_market_price"):
            return self.engine.get_market_price(payload)

        return {
            "market_price": payload.get("price", 0)
        }
