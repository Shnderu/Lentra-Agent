from typing import Dict, Any


class ScenarioPolicyEngine:
    """
    Политика выбора сценария
    """
    def __init__(self, rules: Dict[str, str]):
        self.rules = rules

    def select(self, intent: Dict[str, Any], user_input: Dict[str, Any]) -> str:
        intent_type = intent.get("type")
        if not intent_type:
            return "fallback"

        return self.rules.get(intent_type, "fallback")


# 🔥 ДОБАВЛЯЕМ ОБРАТНУЮ СОВМЕСТИМОСТЬ FACTORY
def build_scenario_policy_engine(registry):
    default_rules = {
        "search": "search_scenario",
        "rent": "rent_scenario",
        "fallback": "fallback_scenario"
    }

    try:
        rules = registry.get("scenario_rules")
        if isinstance(rules, dict):
            default_rules.update(rules)
    except Exception:
        pass

    return ScenarioPolicyEngine(default_rules)
