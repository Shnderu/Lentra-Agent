from lentra.scenarios.registry import scenario_registry

print("[SCENARIO IMPORT] rent_scenario_v1 registry id =", id(scenario_registry))


class RentScenarioV1:
    def execute(self, ctx: dict) -> dict:
        return {
            "scenario": "rent_scenario_v1",
            "ok": True,
            "input": ctx
        }


scenario_registry.register("rent_scenario_v1", RentScenarioV1())
