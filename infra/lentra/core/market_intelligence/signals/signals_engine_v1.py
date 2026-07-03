from typing import Dict, Any


class SignalsEngineV1:
    """
    Deterministic signal extraction layer.

    Converts raw engine output into structured market signals.
    """

    def build(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "pricing": self._pricing_signal(data),
            "risk": self._risk_signal(data),
            "area": self._area_signal(data),
            "dedup": self._dedup_signal(data),
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

    def _risk_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        risk = data.get("risk", {}).get("risk_level", 0)

        # normalize + clamp
        score = min(max(risk, 0.0), 1.0)

        return {
            "score": score,
            "level": "high" if score > 0.7 else "medium" if score > 0.3 else "low"
        }

    def _area_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # placeholder for expat/area intelligence
        return {
            "score": 0.5,
            "note": "baseline_area_proxy"
        }

    def _dedup_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        dedup = data.get("dedup", {}).get("score", 1.0)

        return {
            "score": dedup,
            "confidence": dedup
        }
