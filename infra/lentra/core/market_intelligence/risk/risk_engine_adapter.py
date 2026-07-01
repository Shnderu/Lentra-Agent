from typing import Any, Dict
from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2


class RiskEngineAdapter:
    """
    Contract adapter for IntelligenceGateway.
    Normalizes RiskEngineV2 -> .evaluate(payload)
    """

    def __init__(self):
        self.engine = RiskEngineV2()

    def evaluate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gateway contract method.
        Must return normalized dict:
        {
            "risk_level": str,
            "risk_score": float,
        }
        """
        result = self.engine.run(payload) if hasattr(self.engine, "run") else self.engine.process(payload)

        # normalize output defensively
        if not isinstance(result, dict):
            result = {}

        return {
            "risk_level": result.get("risk_level", "low"),
            "risk_score": result.get("risk_score", 0.0),
        }
