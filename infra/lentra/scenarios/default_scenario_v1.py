from lentra.scenarios.registry import scenario_registry


class DefaultScenarioV1:
    name = "default_v1"

    def execute(self, payload: dict):
        return {
            "scenario": self.name,
            "input": payload,
            "status": "ok"
        }


# register on import (safe now because registry is clean singleton)
scenario_registry.register("default_v1", DefaultScenarioV1())
