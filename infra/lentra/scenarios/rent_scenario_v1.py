from typing import Dict, Any
from lentra.scenarios.registry import scenario_registry


class RentScenarioV1:
    name = "rent_scenario_v1"

    def __init__(self):
        # lazy load to avoid import crash on startup
        self._intelligence = None

    def _get_intelligence(self):
        if self._intelligence is None:
            from lentra.services.market_intelligence_v2 import MarketIntelligenceV2
            self._intelligence = MarketIntelligenceV2()
        return self._intelligence

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        intent = request.get("intent", {})
        query = intent.get("query", "")

        intelligence = self._get_intelligence()

        market = intelligence.analyze(intent)
        price = intelligence.price_check(intent, market)
        risk = intelligence.risk_score(intent, market)
        dedup = intelligence.deduplicate(intent, market)

        return {
            "scenario": self.name,
            "ok": True,
            "input": request,
            "analysis": {
                "query": query,
                "type": "rent"
            },
            "market": market,
            "price": price,
            "dedup": dedup,
            "risk": risk,
            "verdict": intelligence.verdict(price, risk)
        }


scenario_registry.register("rent_scenario_v1", RentScenarioV1())
