from typing import Dict, Any


class RiskSignalProvider:

    name = "risk"

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        pricing = ctx.get("pricing", {})
        coupling = ctx.get("coupling", {})
        dedup = ctx.get("dedup", {})
        area = ctx.get("area", {})

        price_risk = abs(
            pricing.get("deviation", 0)
        )

        duplicate_risk = dedup.get(
            "duplicate_pressure",
            0
        )

        conflict_risk = coupling.get(
            "score",
            0
        )

        area_risk = max(
            0,
            1 - area.get("score", 0.5)
        )

        risk = (
            price_risk * 0.35 +
            duplicate_risk * 0.25 +
            conflict_risk * 0.25 +
            area_risk * 0.15
        )

        risk = max(
            0,
            min(
                1,
                risk
            )
        )

        if risk < 0.3:
            level = "low"
        elif risk < 0.6:
            level = "medium"
        else:
            level = "high"

        return {
            "risk_level": round(risk, 4),
            "score": round(risk, 4),
            "level": level
        }
