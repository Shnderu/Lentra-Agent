from typing import Dict, Any


class EnrichmentLayer:
    """
    ENRICHMENT LAYER v1

    PURPOSE:
    - НЕ участвует в decision
    - НЕ влияет на scoring
    - только добавляет контекст поверх результата pipeline
    - MUST NEVER break API
    """

    def compute(self, result: Dict[str, Any]) -> Dict[str, Any]:

        try:
            enriched = dict(result)

            signals = enriched.get("signals", {})
            pricing = signals.get("pricing", {})

            # ----------------------------
            # enrichment signals (non-critical)
            # ----------------------------

            enriched["enrichment"] = {
                "market_context": self._market_context(pricing),
                "recommendation_hint": self._hint(pricing),
                "meta": {
                    "layer": "enrichment_v1",
                    "safe": True
                }
            }

            return enriched

        except Exception as e:
            # CRITICAL: enrichment NEVER breaks pipeline
            return {
                **result,
                "enrichment_error": str(e)
            }

    def _market_context(self, pricing: Dict[str, Any]) -> str:
        score = pricing.get("score", 0)

        if score > 0.85:
            return "strong_value"
        if score > 0.7:
            return "fair_value"
        return "overpriced"

    def _hint(self, pricing: Dict[str, Any]) -> str:
        direction = pricing.get("direction", "unknown")

        if direction == "over":
            return "negotiate_down"
        if direction == "under":
            return "good_deal"
        return "neutral"
