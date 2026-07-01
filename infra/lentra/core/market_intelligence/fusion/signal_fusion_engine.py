from typing import Dict, Any


class SignalFusionEngine:

    def fuse(self, ui: Dict[str, Any], api: Dict[str, Any], meta: Dict[str, Any]) -> Dict[str, Any]:

        price = ui.get("price", 0)
        market_price = ui.get("market_price", 0)
        deviation = ui.get("deviation_pct", 0)

        risk = ui.get("risk_level", "unknown")
        duplicates = ui.get("duplicates", 0)

        area_score = api.get("signals", {}).get("area_score", 0)

        # ----------------------------
        # BASE SCORE MODEL
        # ----------------------------

        score = 100

        # price pressure
        if deviation > 15:
            score -= 25
        elif deviation > 5:
            score -= 10

        # risk impact
        if risk == "high":
            score -= 30
        elif risk == "medium":
            score -= 15

        # duplication noise
        if duplicates > 5:
            score -= 20
        elif duplicates > 2:
            score -= 10

        # expat quality boost
        if area_score > 8:
            score += 10
        elif area_score < 4:
            score -= 10

        # clamp
        score = max(0, min(100, score))

        # ----------------------------
        # VERDICT ENGINE
        # ----------------------------

        if score >= 80:
            verdict = "strong_buy"
        elif score >= 60:
            verdict = "acceptable"
        elif score >= 40:
            verdict = "overpriced"
        else:
            verdict = "high_risk"

        meta["fusion_score"] = score
        ui["verdict"] = verdict

        return {
            "ui": ui,
            "api": api,
            "meta": meta
        }
