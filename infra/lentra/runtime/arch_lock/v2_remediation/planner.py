from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Violation:
    file: str
    rule: str
    target: str


class V2Planner:
    """
    ARCH LOCK v2.2 - PLAN ONLY ENGINE

    IMPORTANT:
    - NO FILE MODIFICATIONS
    - NO EXECUTION
    - ONLY PLAN OUTPUT
    """

    def build_plan(self, violations: List[Dict[str, Any]]) -> Dict[str, Any]:
        plan = {
            "version": "v2.2",
            "mode": "PLAN_ONLY",
            "actions": []
        }

        for v in violations:
            plan["actions"].append({
                "file": v.get("file"),
                "issue": v.get("rule"),
                "suggested_fix": self._suggest_fix(v)
            })

        return plan

    def _suggest_fix(self, v: Dict[str, Any]) -> str:
        rule = v.get("rule", "")

        if "NO_RUNTIME_TO_CORE" in rule:
            return "Move dependency to runtime.gateway or contracts layer"
        if "bootstrap" in rule:
            return "Redirect bootstrap import to runtime.bootstrap_guard"
        if "graph" in rule:
            return "Route through graph_v2 adapter layer"

        return "Manual review required"
