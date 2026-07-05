from typing import Dict, Any


def build_final_response(ctx) -> Dict[str, Any]:
    """
    SINGLE SOURCE OF TRUTH for API response shape.
    NO engine can bypass this.
    """

    return {
        "pricing": ctx.pricing,
        "area": ctx.area,
        "dedup": ctx.dedup,
        "coupling": ctx.coupling,
        "risk": ctx.risk,
        "ranking": ctx.ranking,
        "enrichment": {
            "market_context": ctx.enrichment.get("market_context", "neutral"),
            "recommendation_hint": ctx.enrichment.get("recommendation_hint", "neutral"),
            "meta": {
                "layer": "enrichment_v2",
                "safe": True
            }
        }
    }
