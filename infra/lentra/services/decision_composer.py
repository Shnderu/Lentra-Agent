from typing import Dict, Any


class DecisionComposer:

    def build(self, intent: Dict[str, Any], market: Dict[str, Any], price: Dict[str, Any], risk: Dict[str, Any], dedup: Dict[str, Any]) -> Dict[str, Any]:

        verdict = self._verdict(price, risk)

        return {
            "object": {
                "query": intent.get("query"),
                "location": intent.get("location"),
                "budget": intent.get("budget_max")
            },
            "market": market,
            "price": price,
            "dedup": dedup,
            "risk": risk,
            "verdict": verdict
        }

    def _verdict(self, price, risk):

        if risk.get("risk_level") == "high":
            return "high_risk_listing"

        if price.get("deviation_pct", 0) > 10:
            return "overpriced_but_ok_location"

        if price.get("deviation_pct", 0) < -10:
            return "good_deal"

        return "market_ok"
