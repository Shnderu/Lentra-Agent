from typing import Dict, Any

from lentra.scenarios.registry import scenario_registry
from lentra.services.intent_normalizer import intent_normalizer
from lentra.core.data_layer.property_model import property_extractor
from lentra.core.data_layer.market_context import market_context_builder
from lentra.services.price_engine import price_engine
from lentra.services.dedup_engine import dedup_engine
from lentra.services.risk_engine import risk_engine


class ScenarioRouter:
    def route(self, intent: Dict[str, Any]) -> str:
        query = (intent.get("query") or "").lower()

        if any(x in query for x in ["studio", "rent", "flat", "apartment", "beach", "cheap"]):
            return "rent_scenario_v1"

        return "default_scenario_v1"


class Pipeline:
    def __init__(self):
        self.router = ScenarioRouter()

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        raw_query = request.get("raw_query", "")

        intent = intent_normalizer.build(raw_query)

        property_obj = property_extractor.extract(intent, raw_query)

        market_context = market_context_builder.build(property_obj.__dict__)

        price_analysis = price_engine.evaluate(
            property_obj.__dict__,
            market_context.__dict__
        )

        dedup = dedup_engine.cluster(property_obj.__dict__)

        risk = risk_engine.evaluate(
            property_obj.__dict__,
            market_context.__dict__
        )

        scenario_name = self.router.route(intent)

        scenario = scenario_registry.get(scenario_name)

        if scenario is None:
            scenario = scenario_registry.get("default_scenario_v1")

        if scenario is None:
            raise RuntimeError("CRITICAL: default_scenario_v1 not registered")

        result = scenario.execute({
            "intent": intent,
            "property": property_obj.__dict__,
            "market": market_context.__dict__,
            "price": price_analysis,
            "dedup": dedup,
            "risk": risk,
            "raw_query": raw_query
        })

        return {
            "entry": scenario_name,
            "intent": intent,
            "property": property_obj.__dict__,
            "market": market_context.__dict__,
            "price": price_analysis,
            "dedup": dedup,
            "risk": risk,
            "result": result
        }


pipeline = Pipeline()
