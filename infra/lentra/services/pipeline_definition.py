from lentra.core.graph.state_runtime_v1 import state_graph_runtime
from lentra.core.scenario.registry import scenario_registry
from lentra.core.router.multi_scenario_router_v1 import MultiScenarioRouterV1


class PipelineDefinition:

    def __init__(self):
        self.router = MultiScenarioRouterV1()

    def execute(self, intent: dict):

        self._ensure_scenarios_loaded()

        # 1. enrich intent with multi-scenario routing
        intent_obj = self._to_object(intent)

        routed_intent = self.router.route(intent_obj)

        # 2. inject resolved scenarios back
        if hasattr(routed_intent, "scenarios"):
            intent["scenarios"] = routed_intent.scenarios

        # 3. execute graph runtime
        return state_graph_runtime.execute(intent)

    def _to_object(self, intent: dict):
        return type("Intent", (), {
            "name": intent.get("name"),
            "confidence": intent.get("confidence", 0.3),
            "payload": intent.get("payload", {}),
            "scenarios": intent.get("scenarios", [])
        })

    def _ensure_scenarios_loaded(self):
        import lentra.scenarios  # noqa

        if not scenario_registry.get("default_scenario_v1"):
            raise Exception("default_scenario_v1 not registered")


pipeline = PipelineDefinition()
