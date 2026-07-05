from typing import Dict, Any


class ExplanationEngineV1:
    """
    Converts raw engine outputs → human-readable reasoning

    PURPOSE:
    - explain ranking
    - explain risk
    - explain pricing deviation
    """

    def explain(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        pricing = ctx.get("pricing", {})
        risk = ctx.get("risk", {})
        ranking = ctx.get("ranking", {})
        coupling = ctx.get("coupling", {})

        explanation = {
            "verdict": self._verdict(ranking.get("score", 0)),
            "why_risk": self._risk_reason(risk),
            "why_price": self._price_reason(pricing),
            "why_coupling": self._coupling_reason(coupling),
        }

        return explanation

    def _verdict(self, score: float) -> str:
        if score > 0.7:
            return "strong_buy_signal"
        if score > 0.4:
            return "moderate_buy_signal"
        return "weak_or_neutral"

    def _risk_reason(self, risk: Dict[str, Any]) -> str:
        r = risk.get("risk_level", 0)
        if r < 0.2:
            return "low_risk_market_aligned"
        if r < 0.5:
            return "medium_risk_some_deviation"
        return "high_risk_warning"

    def _price_reason(self, pricing: Dict[str, Any]) -> str:
        d = pricing.get("deviation", 0)
        if d < 0.1:
            return "price_close_to_market"
        return "price_deviates_from_market"

    def _coupling_reason(self, coupling: Dict[str, Any]) -> str:
        s = coupling.get("score", 0)
        if s < 0.05:
            return "no_strong_cross_signal_conflict"
        return "signal_conflict_present"
