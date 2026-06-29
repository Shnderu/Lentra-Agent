from typing import Dict, Any


class MarketScoringEngine:
    """
    V2 SCORING LAYER:
    consumes signals → produces metrics
    """

    def build_market(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        price_band = {"min": 250, "max": 450}

        if signals["cheap"]:
            price_band = {"min": 180, "max": 350}

        if signals["beach"]:
            price_band["min"] += 80
            price_band["max"] += 120

        risk = 0.3
        if signals["beach"] and signals["cheap"]:
            risk += 0.2

        return {
            "price_band": price_band,
            "risk_score": round(min(0.95, risk), 2),
            "signals": signals
        }

    def price_check(self, market: Dict[str, Any], budget: int) -> Dict[str, Any]:
        avg = (market["price_band"]["min"] + market["price_band"]["max"]) / 2

        deviation = 0
        if budget:
            deviation = ((avg - budget) / budget) * 100

        return {
            "avg_price": avg,
            "deviation_pct": round(deviation, 2),
            "status": "fair"
        }

    def risk(self, market: Dict[str, Any]) -> Dict[str, Any]:
        score = market["risk_score"]

        if score > 0.7:
            level = "high"
        elif score > 0.4:
            level = "medium"
        else:
            level = "low"

        return {
            "risk_score": score,
            "risk_level": level
        }

    def dedup(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        loc = intent.get("location", "unknown")

        return {
            "cluster_id": f"{loc}_cluster_v2",
            "confidence": 0.6,
            "method": "scoring_engine_v2"
        }
