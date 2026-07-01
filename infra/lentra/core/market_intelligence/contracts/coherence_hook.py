from typing import Dict, Any


class CoherenceHook:
    """
    Native extension point inside MarketIntelligenceEngine.
    """

    def __init__(self, checker):
        self.checker = checker

    def apply(self, result: Dict[str, Any]) -> Dict[str, Any]:
        coherence = self.checker.check(result)
        result["meta"]["coherence"] = coherence
        return result
