from typing import Dict, Any, List


class ConflictEngine:

    def resolve(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:

        conflicts = []
        adjustments = {}

        price = self._get(signals, "price")
        market_price = self._get(signals, "market_price")
        risk = self._get(signals, "risk_level")
        expat = self._get(signals, "area_score")
        duplicates = self._get(signals, "duplicates")

        # -------------------------
        # CONFLICT RULE 1
        # overpriced vs low livability
        # -------------------------
        if price > market_price * 1.1 and expat < 5:
            conflicts.append("overprice_low_area")
            adjustments["score_penalty"] = adjustments.get("score_penalty", 0) + 20

        # -------------------------
        # CONFLICT RULE 2
        # low price but high risk
        # -------------------------
        if price < market_price * 0.9 and risk == "high":
            conflicts.append("cheap_scam_signal")
            adjustments["score_penalty"] = adjustments.get("score_penalty", 0) + 30

        # -------------------------
        # CONFLICT RULE 3
        # duplicates distort pricing
        # -------------------------
        if duplicates > 3:
            conflicts.append("high_duplication_noise")
            adjustments["confidence_penalty"] = 0.2

        # -------------------------
        # CONFLICT RULE 4
        # strong expat area offsets risk
        # -------------------------
        if expat > 8 and risk == "medium":
            conflicts.append("expat_risk_buffer")
            adjustments["score_boost"] = adjustments.get("score_boost", 0) + 10

        return {
            "conflicts": conflicts,
            "adjustments": adjustments
        }

    def _get(self, signals, name):
        for s in signals:
            if s.get("name") == name:
                return s.get("value")
        return None
