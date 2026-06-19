from lentra.core.router.multi_scenario_router_v1 import MultiScenarioRouterV1
from lentra.core.scenario.composition_engine_v1 import composition_engine
from lentra.core.graph.state_runtime_v1 import state_graph_runtime
from lentra.core.scenario.scenario_engine_v1 import scenario_engine


router = MultiScenarioRouterV1()


def build_pipeline(intent):

    class Pipeline:
        def execute(self, payload):

            routed = router.route(intent)

            plan = composition_engine.build(intent, routed.scenarios)

            prev = None
            for step in plan:
                if prev:
                    state_graph_runtime.add_edge(prev, step.scenario)
                prev = step.scenario

            result = state_graph_runtime.execute(intent, scenario_engine)

            return {
                "status": "ok",
                "execution": result
            }

    return Pipeline()
