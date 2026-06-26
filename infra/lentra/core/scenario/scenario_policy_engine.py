from typing import Dict, Any


class ScenarioPolicyEngine:
    """
    intent -> scenario mapping + execution contract
    """

    def __init__(self, rules: Dict[str, str]):
        self.rules = rules or {}

    def select(self, intent: Dict[str, Any], user_input: Dict[str, Any]) -> str:
        intent_type = intent.get("type")

        if not intent_type:
            return "fallback"

        return self.rules.get(intent_type, "fallback")

    def run(self, scenario: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "scenario": scenario,
            "context": context,
            "status": "ok"
        }
