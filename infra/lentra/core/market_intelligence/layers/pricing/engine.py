from typing import Dict, Any

class PricingLayer:
    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        payload = dict(payload)

        price = payload.get("price", 0)
        market = payload.get("market_price", price)

        payload["pricing"] = {
            "market_diff": price - market,
            "market_ratio": price / market if market else 1
        }

        return payload
