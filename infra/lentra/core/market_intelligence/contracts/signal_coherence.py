from typing import Dict, Any


class SignalCoherenceChecker:
    """
    Checks cross-signal consistency across engines.
    Pure validation layer, no mutation.
    """

    def check(self, result: Dict[str, Any]) -> Dict[str, Any]:
        ui = result.get("ui", {})
        api = result.get("api", {})
        vector = api.get("vector", {})

        price = ui.get("price", 0)
        market_price = ui.get("market_price")

        deviation = ui.get("deviation_pct", 0.0)

        risk = vector.get("risk_signal", {}).get("risk_level", "unknown")
        expat_area = vector.get("expat_signal", {}).get("area_score", 0.0)

        consistency_flags = {
            "price_valid": price is not None,
            "market_price_valid": market_price is None or market_price > 0,
            "risk_alignment": risk in ["low", "medium", "high", "unknown"],
            "expat_valid": expat_area >= 0.0,
            "deviation_consistency": isinstance(deviation, (int, float)),
        }

        score = sum(1 for v in consistency_flags.values() if v)

        return {
            "is_consistent": score == len(consistency_flags),
            "score": score,
            "max_score": len(consistency_flags),
            "flags": consistency_flags,
        }
