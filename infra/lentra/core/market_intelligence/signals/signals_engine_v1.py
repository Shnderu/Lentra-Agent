from typing import Dict, Any
from lentra.core.market_intelligence.signals.providers.coupling_provider import CouplingSignalProvider
from lentra.core.market_intelligence.signals.providers.risk_provider import RiskSignalProvider
from lentra.core.market_intelligence.signals.providers.ranking_provider import RankingSignalProvider


class SignalsEngineV1:
    """
    Deterministic signal extraction layer (immutable compatible)
    """

    def __init__(self):
        self.risk_provider = RiskSignalProvider()
        self.coupling_provider = CouplingSignalProvider()
        self.ranking_provider = RankingSignalProvider()

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        pricing = self._pricing_signal(data)
        area = self._area_signal(data)
        dedup = self._dedup_signal(data)

        base_inputs = {
            **data,
            "signals": {
                "pricing": pricing,
                "area": area,
            },
            "dedup": dedup,
        }

        coupling = self.coupling_provider.compute(base_inputs)
        risk = self.risk_provider.compute(base_inputs)
        ranking = self.ranking_provider.compute(base_inputs)

        return {
            "pricing": pricing,
            "area": area,
            "dedup": dedup,
            "coupling": coupling,
            "risk": risk,
            "ranking": ranking,
        }

    def _pricing_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("price", 0)
        market = data.get("market_price", 0)

        if not market:
            return {"score": 0.0, "deviation": 0.0}

        deviation = (price - market) / market

        return {
            "score": min(abs(deviation), 1.0),
            "direction": "over" if deviation > 0 else "under",
            "deviation": round(deviation, 4),
        }

    def _area_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "score": 0.5,
            "note": "enhanced_area_model"
        }

    def _dedup_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        dedup = data.get("dedup", {}).get("score", 1.0)
        return {
            "score": dedup,
            "confidence": dedup
        }
