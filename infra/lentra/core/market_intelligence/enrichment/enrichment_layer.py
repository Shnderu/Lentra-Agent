from typing import Dict, Any


class EnrichmentLayer:
    """
    V2 Enrichment Layer

    PURPOSE:
    - DO NOT recompute signals
    - ONLY add semantic interpretation layer
    """

    def compute(self, signals: Dict[str, Any]) -> Dict[str, Any]:

        pricing = signals.get("pricing", {})
        risk = signals.get("risk", {})
        ranking = signals.get("ranking", {})

        market_context = self._market_context(pricing, risk)
        recommendation = self._recommendation(risk, ranking)

        return {
            "market_context": market_context,
            "recommendation_hint": recommendation,
            "meta": {
                "layer": "enrichment_v2",
                "safe": True
            }
        }

    def _market_context(self, pricing, risk):
        if pricing.get("score", 0) > 0.8:
            return "extreme_overpriced"
        if pricing.get("direction") == "over":
            return "overpriced"
        return "fair"

    def _recommendation(self, risk, ranking):
        risk_score = risk.get("score", 0)

        if risk_score > 0.7:
            return "avoid"
        if risk_score > 0.3:
            return "caution"
        return "neutral"
