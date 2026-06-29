from lentra.core.market_intelligence.models.market_object import MarketObject


class VerdictEngine:

    def run(self, obj):

        # normalize input (dict or object-safe)
        risk = getattr(obj, "risk", None)
        if risk is None and isinstance(obj, dict):
            risk = obj.get("risk", 0.5)
        if risk is None:
            risk = 0.5

        area_score = getattr(obj, "area_score", None)
        if area_score is None and isinstance(obj, dict):
            area_score = obj.get("area_score", 5.0)
        if area_score is None:
            area_score = 5.0

        price_deviation = getattr(obj, "price_deviation", None)
        if price_deviation is None and isinstance(obj, dict):
            price_deviation = obj.get("price_deviation", 0.0)
        if price_deviation is None:
            price_deviation = 0.0

        score = 0.5

        # risk impact
        score -= float(risk) * 0.4

        # area impact
        score += (float(area_score) - 5.0) * 0.05

        # price deviation impact
        score -= abs(float(price_deviation)) * 0.3

        # clamp
        if score < 0:
            score = 0.0
        if score > 1:
            score = 1.0

        verdict = (
            "strong_buy" if score >= 0.75 else
            "good_deal" if score >= 0.6 else
            "neutral" if score >= 0.4 else
            "overpriced" if score >= 0.25 else
            "avoid"
        )

        # write back safely
        if isinstance(obj, dict):
            obj["verdict"] = verdict
            obj["confidence"] = round(score, 3)
        else:
            obj.verdict = verdict
            obj.confidence = round(score, 3)

        return obj
