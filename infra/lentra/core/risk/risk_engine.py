from typing import Dict, Any, List


class RiskEngine:
    """
    VIETNAM RENTAL RISK ENGINE

    Outputs:
    - risk_score (0-100)
    - risk_level (low/medium/high)
    - signals (explanations)
    """

    def evaluate(
        self,
        item: Dict[str, Any],
        market_stats: Dict[str, Any],
        duplicate_count: int = 1
    ) -> Dict[str, Any]:

        signals = []
        score = 0

        # -------------------------
        # 1. PRICE ANOMALY
        # -------------------------
        deviation = item.get("deviation_pct")

        if deviation is not None:
            if abs(deviation) > 40:
                score += 40
                signals.append("extreme_price_deviation")
            elif abs(deviation) > 20:
                score += 20
                signals.append("high_price_deviation")

        # -------------------------
        # 2. DUPLICATION RISK
        # -------------------------
        if duplicate_count >= 5:
            score += 30
            signals.append("high_duplicate_frequency")
        elif duplicate_count >= 3:
            score += 15
            signals.append("moderate_duplicate_frequency")

        # -------------------------
        # 3. MISSING DATA RISK
        # -------------------------
        if not item.get("images"):
            score += 10
            signals.append("missing_images")

        if not item.get("contact"):
            score += 10
            signals.append("missing_contact_info")

        # -------------------------
        # 4. FINAL SCORE
        # -------------------------
        risk_score = min(score, 100)

        if risk_score >= 70:
            level = "high"
        elif risk_score >= 40:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_score": risk_score,
            "risk_level": level,
            "signals": signals
        }
