from typing import Dict, Any


class PriceDeviationEngine:
    def evaluate(self, property_obj: Dict[str, Any], market: Dict[str, Any]) -> Dict[str, Any]:
        budget = property_obj.get("budget_max") or 0
        avg_price = market.get("avg_price") or 0

        if budget == 0 or avg_price == 0:
            return {
                "status": "unknown",
                "deviation": None
            }

        deviation = ((budget - avg_price) / avg_price) * 100

        if deviation >= 10:
            status = "cheap"
        elif deviation <= -10:
            status = "expensive"
        else:
            status = "fair"

        return {
            "status": status,
            "deviation_pct": round(deviation, 2)
        }


price_engine = PriceDeviationEngine()
