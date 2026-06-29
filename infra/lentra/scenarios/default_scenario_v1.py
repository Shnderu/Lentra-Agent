from typing import Dict, Any
from lentra.scenarios.registry import scenario_registry


class DefaultScenarioV1:
    name = "default_scenario_v1"

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "scenario": self.name,
            "ok": True,
            "input": request
        }


# auto-register
scenario_registry.register("default_scenario_v1", DefaultScenarioV1())
