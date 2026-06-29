from lentra.core.scenario.scenario_engine_impl import scenario_engine_impl


class ScenarioEngineV1:

    def execute(self, node, state):
        return scenario_engine_impl(node, state)


scenario_engine = ScenarioEngineV1()
