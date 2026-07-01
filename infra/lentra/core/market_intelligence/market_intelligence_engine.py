from typing import Dict, Any

from lentra.core.market_intelligence.output import MarketIntelligenceOutputFacade
from lentra.core.market_intelligence.decision.integrated_signal_decision import IntegratedSignalDecision


class MarketIntelligenceEngine:
    """
    Canonical Market Intelligence Engine (LOCKED V1)

    Flow:
        input → enrich → signals → decision → output contract
    """

    def __init__(self):
        self.output_facade = MarketIntelligenceOutputFacade()
        self.decision = IntegratedSignalDecision()

    def analyze(self, payload: Dict[str, Any]):
        enriched = self._enrich(payload)
        decision = self.decision.build(enriched)

        final_context = {
            **enriched,
            "signals": decision["signals"],
            "dominant_signal": decision["dominant_signal"],
            "decision_flags": decision["decision_flags"],
            "authority_score": decision["authority_score"],
        }

        return self.output_facade.analyze(final_context)

    def _enrich(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price": payload.get("price"),
            "market_price": payload.get("market_price", 650),
            "deviation_pct": payload.get("deviation_pct", 0.07),
            "risk_score": payload.get("risk_score", 0.5),
            "duplicates": payload.get("duplicates", 0),
            "staleness": payload.get("staleness", 0.2),
            "price_trend": payload.get("price_trend", 0.0),
            "area": payload.get("area", {
                "internet": 7.5,
                "noise": 5.0,
                "expat_density": 6.5
            }),
        }
