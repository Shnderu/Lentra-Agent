from typing import Dict, Any


class RankingSignalProvider:

    name = "ranking"

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        pricing = ctx.get("pricing", {})
        area = ctx.get("area", {})
        risk = ctx.get("risk", {})
        coupling = ctx.get("coupling", {})
        dedup = ctx.get("dedup", {})

        price_quality = 1.0 - pricing.get("score", 0.5)
        area_quality = area.get("score", 0.5)

        risk_penalty = risk.get("score", 0.0)
        coupling_penalty = coupling.get("score", 0.0)
        dedup_conf = dedup.get("confidence", 1.0)

        score = (
            price_quality *
            area_quality *
            (1.0 - risk_penalty) *
            (1.0 - coupling_penalty) *
            dedup_conf
        )

        return {
            "score": round(score, 5),
            "components": {
                "price_quality": price_quality,
                "area_quality": area_quality,
                "risk_penalty": risk_penalty,
                "coupling_penalty": coupling_penalty,
                "dedup_confidence": dedup_conf
            },
            "version": "ranking_v2"
        }
