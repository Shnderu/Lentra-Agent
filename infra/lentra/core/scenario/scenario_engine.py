from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ScenarioResult:
    scenario_id: str
    confidence: float = 1.0


class ScenarioEngine:
    """
    SCENARIO LAYER = PURE ROUTING CLASSIFIER

    Архитектурное правило:
    - НЕ принимает решений о бизнес-логике
    - НЕ вызывает core intelligence
    - НЕ влияет на execution flow напрямую
    """

    def __init__(self):
        # статическая таблица маршрутов (можно расширять позже)
        self.route_map = {
            "search": "scenario_search_v1",
            "analysis": "scenario_analysis_v1",
            "alert": "scenario_alert_v1",
            "default": "scenario_default_v1"
        }

    def resolve(self, intent: str, context: Optional[Dict] = None) -> ScenarioResult:
        """
        Единственная задача:
        intent → scenario_id
        """

        scenario_id = self.route_map.get(intent, self.route_map["default"])

        return ScenarioResult(
            scenario_id=scenario_id,
            confidence=1.0
        )
