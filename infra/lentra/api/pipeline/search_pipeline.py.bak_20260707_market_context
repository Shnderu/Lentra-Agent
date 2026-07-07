from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3


class SearchPipeline:
    """
    Single entrypoint for /search API
    """

    def __init__(self):
        self.gateway = build_gateway_v3()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pipeline flow:
        1. normalize input (lightweight)
        2. execute engines
        3. assemble response
        """

        context = {
            "query": payload.get("query"),
            "price": payload.get("price"),
            "market_price": payload.get("market_price"),
        }

        # ENGINE EXECUTION LAYER
        area = self.gateway.run_engine("area", context)
        market = self.gateway.run_engine("market_intelligence", context)

        # SIGNAL COMBINATION (minimal safe merge)
        features = {
            "area": area,
            "market_intelligence": market,
        }

        # DECISION LAYER (temporary inline policy until Phase 2)
        score = 0.5

        if isinstance(market, dict) and "score" in market:
            score = float(market["score"])

        decision = "BUY" if score >= 0.6 else "AVOID"

        return {
            "query": context["query"],
            "features": features,
            "decision": {
                "decision": decision,
                "final_score": score,
                "confidence": 0.5
            }
        }
