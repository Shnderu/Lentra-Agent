from typing import Dict, Any

from lentra.scenarios.registry import scenario_registry
from lentra.services.intent_normalizer import intent_normalizer
from lentra.core.data_layer.property_model import property_extractor
from lentra.core.data_layer.market_context import market_context_builder
from lentra.services.price_engine import price_engine
from lentra.services.dedup_engine import dedup_engine
from lentra.services.risk_engine import risk_engine


def safe(obj):
    if obj is None:
        return {}

    if isinstance(obj, dict):
        return obj

    if hasattr(obj, "__dict__"):
        return obj.__dict__

    return obj


class ScenarioRouter:
    def route(self, intent: Dict[str, Any]) -> str:
        query = (intent.get("query") or "").lower()

        if any(word in query for word in (
            "studio",
            "rent",
            "flat",
            "apartment",
            "beach",
            "cheap",
        )):
            return "rent_scenario_v1"

        return "default_scenario_v1"


class Pipeline:
    def __init__(self):
        self.router = ScenarioRouter()

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        print("[DEBUG] registry keys:", scenario_registry.dump())

        # API передает raw_query
        raw_query = request.get("raw_query", "")

        intent = intent_normalizer.build(raw_query)

        property_obj = property_extractor.extract(intent, raw_query)
        property_dict = safe(property_obj)

        market_context = market_context_builder.build(property_dict)
        market_dict = safe(market_context)

        price_analysis = safe(
            price_engine.analyze(property_dict, market_dict)
        )

        dedup = safe(
            dedup_engine.cluster(property_dict)
        )

        risk = safe(
            risk_engine.evaluate(property_dict, market_dict)
        )

        scenario_name = self.router.route(intent)

        print("[DEBUG] scenario_name:", scenario_name)
        print("[DEBUG] registry dump:", scenario_registry.dump())

        scenario = scenario_registry.get(scenario_name)

        if scenario is None:
            scenario = scenario_registry.get("default_scenario_v1")

        if scenario is None:
            return {
                "entry": "system_fallback",
                "result": {
                    "ok": False,
                    "error": "no_scenario_registered",
                },
            }

        result = scenario.execute(
            {
                "intent": intent,
                "property": property_dict,
                "market": market_dict,
                "price": price_analysis,
                "dedup": dedup,
                "risk": risk,
                "raw_query": raw_query,
            }
        )

        return {
            "entry": scenario_name,
            "intent": intent,
            "property": property_dict,
            "market": market_dict,
            "price": price_analysis,
            "dedup": dedup,
            "risk": risk,
            "result": result,
        }


pipeline = Pipeline()
