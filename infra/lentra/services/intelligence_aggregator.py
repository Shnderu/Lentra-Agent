from typing import Dict, Any


class IntelligenceAggregator:
    """
    v1: single decision layer for rental intelligence OS
    """

    def build_verdict(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        price_dev = analysis.get("price_deviation_pct")
        risk = analysis.get("risk_score", 0)

        score = 0

        if price_dev is not None:
            if price_dev > 10:
                score += 2
            elif price_dev < -10:
                score -= 2

        if risk >= 0.6:
            score += 2
        elif risk <= 0.3:
            score -= 1

        if score <= -2:
            verdict = "UNDERVALUED"
        elif -2 < score <= 1:
            verdict = "FAIR"
        else:
            verdict = "OVERPRICED"

        return {
            "final_score": score,
            "verdict": verdict,
            "confidence": 0.7 if price_dev is not None else 0.5
        }


intelligence_aggregator = IntelligenceAggregator()
