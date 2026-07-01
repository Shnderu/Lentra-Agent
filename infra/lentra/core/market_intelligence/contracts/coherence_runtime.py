from typing import Dict, Any
from lentra.core.market_intelligence.contracts.signal_coherence import SignalCoherenceChecker


class CoherenceRuntime:
    def __init__(self):
        self.checker = SignalCoherenceChecker()

    def execute(self, result: Dict[str, Any]) -> Dict[str, Any]:
        result["meta"]["coherence"] = self.checker.check(result)
        return result
