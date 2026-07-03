from typing import Dict, Any


class RiskSignalProvider:
    """
    Risk Engine v2.3 (Coupling-aware amplifier)

    Now:
    - base risk stable
    - anti-scam preserved
    - coupling acts as amplifier ONLY
    """

    name = "risk"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:

        price_risk = self._price_risk(engine_outputs)
        area_risk = self._area_risk(engine_outputs)
        dup_risk = self._dup_risk(engine_outputs)
        heuristic = self._heuristic(engine_outputs)

        coupling = engine_outputs.get("coupling", {}).get("score", 0.0)

        base_risk = (
            price_risk * 0.35 +
            area_risk * 0.25 +
            dup_risk * 0.20 +
            heuristic * 0.10 +
            coupling * 0.10
        )

        anti_scam = self._anti_scam_overlay(engine_outputs)

        final_risk = base_risk * 0.85 + anti_scam * 0.15
        final_risk = self._clamp(final_risk)

        return {
            "risk_level": round(final_risk, 5),
            "score": round(final_risk, 5),
            "level": self._level(final_risk),
            "components": {
                "price_risk": round(price_risk, 4),
                "area_risk": round(area_risk, 4),
                "duplication": round(dup_risk, 4),
                "heuristic": round(heuristic, 4),
                "coupling": round(coupling, 4),
                "anti_scam_overlay": round(anti_scam, 4),
                "base_risk": round(base_risk, 4),
            }
        }

    def _price_risk(self, e: Dict[str, Any]) -> float:
        price = e.get("price", 0)
        market = e.get("market_price", 0)
        if not market:
            return 0.0
        return min(abs(price - market) / market, 1.0)

    def _area_risk(self, e: Dict[str, Any]) -> float:
        area = e.get("signals", {}).get("area", {}) or e.get("area", {})
        if not area:
            return 0.2
        return 1.0 - max(min(area.get("score", 0.5), 1.0), 0.0)

    def _dup_risk(self, e: Dict[str, Any]) -> float:
        dedup = e.get("dedup", {}).get("score", 1.0)
        return 1.0 - dedup

    def _heuristic(self, e: Dict[str, Any]) -> float:
        return 0.1

    def _anti_scam_overlay(self, e: Dict[str, Any]) -> float:
        query = (e.get("query") or "").lower()

        risk = 0.0

        if any(k in query for k in ["whatsapp", "telegram", "viber"]):
            risk += 0.25

        if any(k in query for k in ["urgent", "today", "fast deal"]):
            risk += 0.2

        if any(k in query for k in ["deposit", "booking fee", "caution"]):
            risk += 0.25

        price = e.get("price", 0)
        market = e.get("market_price", 0)

        if price and market:
            ratio = price / market

            if ratio < 0.5:
                risk += 0.4
            if ratio > 2.0:
                risk += 0.2

        return min(risk, 1.0)

    def _clamp(self, x: float) -> float:
        return max(0.0, min(x, 1.0))

    def _level(self, score: float) -> str:
        if score > 0.7:
            return "high"
        if score > 0.3:
            return "medium"
        return "low"
