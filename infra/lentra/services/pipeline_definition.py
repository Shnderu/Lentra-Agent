from typing import Dict, Any

from lentra.scenarios.registry import scenario_registry

from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.market_intelligence.search.parsers.query_parser import QueryParser


class ScenarioRouter:
    def route(self, intent: Dict[str, Any]) -> str:
        q = (intent.get("query") or "").lower()

        if any(x in q for x in ["studio", "rent", "apartment", "flat", "beach"]):
            return "rent_scenario_v1"

        return "default_scenario_v1"


class Pipeline:

    def __init__(self):
        self.router = ScenarioRouter()
        self.intel = MarketIntelligenceEngine()
        self.parser = QueryParser()

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:

        raw_query = request.get("raw_query", "")

        intent = self.parser.parse(raw_query)

        # unified intelligence layer (ВАЖНО)
        intelligence = self.intel.analyze({
            "intent": intent,
            "raw_query": raw_query
        })

        scenario_name = self.router.route(intent)

        scenario = scenario_registry.get(scenario_name)

        if scenario is None:
            scenario = scenario_registry.get("default_scenario_v1")

        if scenario is None:
            return {
                "entry": "system_fallback",
                "result": {"ok": False, "error": "no_scenario_registered"}
            }

        result = scenario.execute({
            "intent": intent,
            "intelligence": intelligence,
            "raw_query": raw_query
        })

        return {
            "entry": scenario_name,
            "intent": intent,
            "intelligence": intelligence,
            "result": result
        }


pipeline = Pipeline()
