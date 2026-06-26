from dataclasses import dataclass, field
from typing import Optional, Any, Dict


@dataclass
class Query:
    text: str
    country: str = "Vietnam"
    intent: str = "unknown"
    budget: Optional[tuple[int, int]] = None
    location: Optional[str] = None
    meta: dict = field(default_factory=dict)


class ScenarioEngineV1:

    def __init__(self):
        pass

    def select(self, intent: dict, user_input: dict) -> str:
        t = intent.get("type", "fallback")

        if t == "rent_search":
            return "rent_search"
        if t == "city_compare":
            return "city_compare"
        if t == "alert":
            return "alert"
        if t == "expat":
            return "expat"

        return "fallback"

    def execute(self, scenario: str, user_input: dict) -> dict:

        if scenario == "fallback":
            return {
                "type": "fallback",
                "message": "no scenario matched"
            }

        if scenario == "rent_search":
            return {
                "type": "rent_search",
                "results": [],
                "insights": []
            }

        if scenario == "city_compare":
            return {
                "type": "city_compare",
                "cities": {}
            }

        if scenario == "alert":
            return {
                "type": "alert",
                "trigger_rules": {}
            }

        if scenario == "expat":
            return {
                "type": "expat",
                "results": []
            }

        return {
            "type": "unknown_scenario"
        }
