from typing import Dict, Any


class RiskSignalProvider:

    name = "risk"

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        pricing = ctx.get("pricing", {})
        area = ctx.get("area", {})
        coupling = ctx.get("coupling", {})

        risk = (
            pricing.get("score", 0.5) * 0.4 +
            area.get("score", 0.5) * 0.3 +
            coupling.get("score", 0.0) * 0.3
        )

        return {
            "risk_level": risk,
            "score": risk,
            "level": "low" if risk < 0.3 else "medium"
        }
