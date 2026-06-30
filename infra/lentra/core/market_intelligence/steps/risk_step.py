from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class RiskResult:
    score: float
    flags: List[str]


class RiskStep:
    """
    LOCK 4: unified risk interface
    """

    def analyze(self, item: Dict[str, Any]) -> Dict[str, Any]:
        price = item.get("price", 0)

        # простая стабилизация риска (MVP-safe)
        score = 0.2 if price < 500 else 0.5 if price < 1500 else 0.8

        item["risk"] = {
            "score": score,
            "flags": []
        }

        return item
