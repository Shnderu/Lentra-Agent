from lentra.scenarios.registry import scenario_registry

print("[SCENARIO IMPORT] default_scenario_v1 registry id =", id(scenario_registry))


class DefaultScenarioV1:
    def execute(self, ctx: dict) -> dict:
        return {
            "scenario": "default_scenario_v1",
            "ok": True,
            "input": ctx
        }


scenario_registry.register("default_scenario_v1", DefaultScenarioV1())
