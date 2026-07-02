from typing import Dict, Any
from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2


class RiskEngineAdapter:
    """
    Унифицированный контракт для IntelligenceGateway.
    Оборачивает RiskEngineV2 (process → evaluate)
    """

    def __init__(self):
        self.engine = RiskEngineV2()

    def evaluate(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        result = self.engine.process(listing)

        return {
            "risk_level": result.get("risk", 0.5),
            "deviation_pct": result.get("deviation", 0.0),
            "raw": result,
        }
