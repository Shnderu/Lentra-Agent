from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from lentra.scenarios.registry import scenario_registry


@dataclass
class ScenarioResultV2:
    data: Dict[str, Any]
    next: List[str]
    meta: Optional[Dict[str, Any]] = None


class ScenarioEngineV1:

    def execute_node(self, node, state):

        handler = scenario_registry.get(node)

        if handler is None:
            return ScenarioResultV2(
                data={"error": f"scenario_not_found:{node}"},
                next=[],
                meta={"status": "missing"}
            )

        result = handler(state) or {}

        # -------------------------
        # normalize contract v2
        # -------------------------
        return ScenarioResultV2(
            data=result.get("data", result),
            next=result.get("next", []),
            meta=result.get("meta", {})
        )

    def execute(self, node, state):
        return self.execute_node(node, state)


scenario_engine = ScenarioEngineV1()
