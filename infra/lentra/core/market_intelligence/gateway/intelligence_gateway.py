from typing import Any, Dict


class IntelligenceGateway:
    def __init__(self, routing_map=None, orchestrator=None):
        self.routing_map = routing_map
        self.orchestrator = orchestrator

    def run(self, engines: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:

        pricing = engines["pricing"].evaluate(payload)
        risk = engines["risk"].evaluate(payload)
        expat = engines["expat"].evaluate(payload)
        dedup = engines["dedup"].evaluate(payload)

        ui = {
            "price": pricing.get("price"),
            "market_price": pricing.get("market_price"),
            "deviation_pct": pricing.get("deviation_pct"),
            "risk_level": risk.get("risk_level"),
            "duplicates": dedup.get("duplicates"),
            "verdict": pricing.get("signal"),
        }

        api = {
            "pricing": pricing,
            "risk": risk,
            "expat": expat,
            "dedup": dedup,
        }

        meta = {
            "trace_id": "gateway-v1",
            "contract": "locked",
        }

        return {
            "ui": ui,
            "api": api,
            "meta": meta,
        }
