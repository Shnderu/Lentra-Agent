from lentra.scenarios.registry import scenario_registry


class ScenarioEngineV1:

    def execute_node(self, node, state):

        handler = scenario_registry.get(node)

        if handler is None:
            return {
                "data": {
                    "error": f"scenario_not_found:{node}"
                },
                "next": []
            }

        result = handler(state) or {}

        # -------------------------
        # normalize output contract
        # -------------------------
        data = result.get("data", result)
        nxt = result.get("next", [])

        # -------------------------
        # mutate state (CRITICAL FIX)
        # -------------------------
        if isinstance(data, dict):
            state.data.update(data)

        return {
            "data": data,
            "next": nxt
        }

    def execute(self, node, state):
        return self.execute_node(node, state)


scenario_engine = ScenarioEngineV1()
