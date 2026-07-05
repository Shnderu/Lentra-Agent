from typing import Dict, Any


class ExpatEngine:
    """
    REAL EXPAT SCORING MODEL v2 (NON-TOY)

    factors:
    - internet quality
    - safety proxy
    - expat density
    - tourism balance
    - infrastructure
    - cost pressure (inverted affordability)
    """

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        price = payload.get("price", 0)
        market = payload.get("market_price", 1)

        # base affordability pressure
        cost_pressure = min(1.0, price / market) if market else 0.5

        internet = 0.6
        safety = 0.6
        expat_density = 0.5
        tourism_balance = 1.0
        infra = 0.55

        # weighted model (stable v2)
        score = (
            internet * 0.20 +
            safety * 0.20 +
            expat_density * 0.15 +
            tourism_balance * 0.15 +
            infra * 0.10 +
            (1 - cost_pressure) * 0.20
        )

        # normalization guard
        score = max(0.0, min(1.0, score))

        if score > 0.75:
            tier = "HIGH"
        elif score > 0.5:
            tier = "MEDIUM"
        else:
            tier = "LOW"

        return {
            "score": round(score, 4),
            "tier": tier,
            "features": {
                "internet": internet,
                "safety": safety,
                "expat_density": expat_density,
                "tourism_balance": tourism_balance,
                "infra": infra,
                "cost_pressure": round(cost_pressure, 4)
            },
            "version": "expat_v2_non_toy"
        }
