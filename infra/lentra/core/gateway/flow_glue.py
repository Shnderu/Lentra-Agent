from typing import Any


class FlowGlue:
    """
    STABLE CONTRACT LAYER
    DO NOT CHANGE SIGNATURE OUTSIDE THIS FILE
    """

    def __init__(
        self,
        intent_resolver: Any,
        intent_router: Any,
        scenario_policy_engine: Any,
        scenario_engine: Any,
    ):
        self.intent_resolver = intent_resolver
        self.intent_router = intent_router
        self.scenario_policy_engine = scenario_policy_engine
        self.scenario_engine = scenario_engine

    def route(self, intent: str, context: dict):
        resolved = self.intent_resolver.resolve(intent, context)
        feature = self.intent_router.route(resolved)
        return feature

    def execute(self, scenario, context):
        return self.scenario_engine.run(scenario, context)
