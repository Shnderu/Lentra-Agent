from typing import Dict, Any


class CouplingSignalProvider:
    """
    Coupling Layer (Market Coherence Amplifier)

    Purpose:
    - detect inconsistency between signals
    - amplify risk when signals conflict
    - stay NON-invasive (does not replace risk)
    """

    name = "coupling"

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:

        price = engine_outputs.get("price", 0)
        market = engine_outputs.get("market_price", 0)

        area = engine_outputs.get("signals", {}).get("area", {})
        dedup = engine_outputs.get("dedup", {})
        risk = engine_outputs.get("risk", {})

        price_risk = self._price_deviation(price, market)
        area_score = area.get("score", 0.5)

        dedup_score = dedup.get("score", 1.0)
        base_risk = risk.get("risk_level", 0.2)

        # -------------------------
        # COUPLING SIGNALS
        # -------------------------

        price_area_mismatch = price_risk * (1.0 - area_score)

        duplication_pressure = (1.0 - dedup_score) * 0.5

        market_conflict = abs(base_risk - price_risk) * 0.3

        score = (
            price_area_mismatch * 0.5 +
            duplication_pressure * 0.3 +
            market_conflict * 0.2
        )

        return {
            "score": round(min(score, 1.0), 5),
            "factors": {
                "price_area_mismatch": round(price_area_mismatch, 5),
                "duplication_pressure": round(duplication_pressure, 5),
                "market_conflict": round(market_conflict, 5),
            }
        }

    def _price_deviation(self, price: float, market: float) -> float:
        if not market:
            return 0.0
        return min(abs(price - market) / market, 1.0)
