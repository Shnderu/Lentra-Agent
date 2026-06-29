from typing import Dict, Any
from lentra.scenarios.registry import scenario_registry
from lentra.services.intelligence_orchestrator import MarketIntelligenceOrchestrator


class RentScenarioV1:
    name = "rent_scenario_v1"

    def __init__(self):
        self.intelligence = MarketIntelligenceOrchestrator()

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:

        intent = request.get("intent", {})
        query = intent.get("query", "")

        intelligence = self.intelligence.analyze(intent)

        market = intelligence["market"]
        price = intelligence["price"]
        dedup = intelligence["dedup"]
        risk = intelligence["risk"]

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

            "verdict": self._build_verdict(price, risk)
        }

    def _build_verdict(self, price, risk):

        if risk.get("risk_level") == "high":
            return "high_risk_listing"

        if price.get("deviation_pct", 0) > 10:
            return "overpriced_but_ok_location"

        if price.get("deviation_pct", 0) < -15:
            return "good_deal"

        return "market_ok"


scenario_registry.register("rent_scenario_v1", RentScenarioV1())
