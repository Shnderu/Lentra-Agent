from typing import Dict, Any
from lentra.core.market_intelligence.isolation.engine_isolator import EngineIsolator


class IntelligenceGateway:
    def __init__(self, engines: Dict[str, Any], graph: Dict[str, Any]):
        self.isolator = EngineIsolator(engines)
        self.graph = graph

    def handle(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        engine_results = self.isolator.run(payload)

        # pricing must always exist
        pricing = engine_results.get("pricing", {})

        return {
            "query": payload.get("query"),
            "pricing": pricing,
            **engine_results
        }
