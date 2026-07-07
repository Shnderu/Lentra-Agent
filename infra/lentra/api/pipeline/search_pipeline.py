from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.market_intelligence.search.parsers.query_parser import parse_query


class SearchPipeline:
    """
    Single entrypoint for /search API.

    Flow:

    User query
        |
        v
    Query Parser
        |
        v
    Market Context
        |
        v
    GatewayV3
        |
        v
    Market Intelligence
    """

    def __init__(self):
        self.gateway = build_gateway_v3()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        query = payload.get("query", "")

        parsed = parse_query(query)

        context = {
            "query": query,

            # market context
            "city": parsed.get("city"),
            "budget": parsed.get("budget"),

            # MVP:
            # budget acts as listing price candidate
            "price": parsed.get("budget", 0),

            # city profile market price
            "market_price": parsed.get(
                "market_price",
                0
            ),
        }

        area = self.gateway.run_engine(
            "area",
            context
        )

        market = self.gateway.run_engine(
            "market_intelligence",
            context
        )

        features = {
            "area": area,
            "market_intelligence": market,
        }

        score = 0.5

        if isinstance(market, dict):
            score = float(
                market.get(
                    "pricing_score",
                    0.5
                )
            )

        decision = (
            "BUY"
            if score >= 0.6
            else "AVOID"
        )

        return {
            "query": query,

            "market_context": context,

            "features": features,

            "decision": {
                "decision": decision,
                "final_score": round(
                    score,
                    4
                ),
                "confidence": market.get(
                    "confidence",
                    0
                ) if isinstance(
                    market,
                    dict
                ) else 0
            }
        }
