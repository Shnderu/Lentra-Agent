from typing import Dict, Any


class RankingSignalProvider:
    """
    Ranking v2 SAFE CONTRACT VERSION
    """

    name = "ranking"

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        pricing = ctx.get("signals", {}).get("pricing", {})
        area = ctx.get("signals", {}).get("area", {})
        risk = ctx.get("risk", {})
        coupling = ctx.get("coupling", {})
        dedup = ctx.get("dedup", {})

        price_quality = self._invert(pricing.get("score", 0.5))
        area_quality = area.get("score", 0.5)

        risk_score = risk.get("risk_level", 0.5)
        coupling_score = coupling.get("score", 0.0)

        dedup_conf = dedup.get("confidence", 1.0)

        ranking = (
            price_quality *
            area_quality *
            (1.0 - risk_score) *
            (1.0 - coupling_score) *
            dedup_conf
        )

        ranking = self._soft_clip(ranking)

        return {
            "score": round(ranking, 5),
            "components": {
                "price_quality": round(price_quality, 4),
                "area_quality": round(area_quality, 4),
                "risk_penalty": round(risk_score, 4),
                "coupling_penalty": round(coupling_score, 4),
                "dedup_confidence": round(dedup_conf, 4),
            },
            "version": "ranking_v2_safe"
        }

    def _invert(self, x: float) -> float:
        return max(0.0, 1.0 - x)

    def _soft_clip(self, x: float) -> float:
        if x < 0.05:
            return 0.05
        return min(x, 1.0)
