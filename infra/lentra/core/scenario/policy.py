from typing import Dict, Any
from lentra.core.scenario.scenario_policy_engine import ScenarioPolicyEngine


def build_scenario_policy_engine(registry):
    """
    Factory слой DI.

    Сейчас registry НЕ содержит стабильного rules layer,
    поэтому используем safe default.
    """

    # безопасные дефолтные правила (минимально жизнеспособные)
    default_rules = {
        "search": "search_scenario",
        "rent": "rent_scenario",
        "fallback": "fallback_scenario"
    }

    # если позже появится registry.rules — можно подключить сюда
    try:
        rules = registry.get("scenario_rules")
        if isinstance(rules, dict):
            default_rules.update(rules)
    except Exception:
        pass

    return ScenarioPolicyEngine(rules=default_rules)
