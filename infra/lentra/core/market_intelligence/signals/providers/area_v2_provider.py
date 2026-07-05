from typing import Dict, Any


class AreaProviderV2:
    """
    Area Intelligence v2 (MVP)

    Upgrade:
    - introduces expat-aware weighting
    - keeps deterministic behavior
    """

    def compute(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        price = engine_outputs.get("price", {})
        base_score = 0.8

        # stable geo defaults
        city = engine_outputs.get("city", "da_nang")

        # deterministic modifiers
        tourism_weight = 0.9 if city == "da_nang" else 0.7
        cost_index = 0.75

        expat_adjustment = 0.05 if tourism_weight > 0.85 else 0.0

        score = base_score * tourism_weight + cost_index * 0.1 + expat_adjustment

        return {
            "score": round(score, 4),
            "city": city,
            "country": "Vietnam",
            "weights": {
                "expat_density": tourism_weight,
                "tourism": tourism_weight,
                "cost_index": cost_index
            },
            "version": "area_v2"
        }
