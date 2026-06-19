from lentra.scenarios.registry import scenario_registry


class ScenarioEngineV1:

    def execute_node(self, node, state):

        handler = scenario_registry.get(node)

        if handler is None:
            return {
                "error": f"scenario_not_found:{node}"
            }

        result = handler(state)

        if result is None:
            result = {}

        return result

    def execute(self, node, state):
        return self.execute_node(node, state)


scenario_engine = ScenarioEngineV1()
