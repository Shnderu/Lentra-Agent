
class ExplanationEngine:

    def run(self, obj):

        reasons = []

        if obj.market_price and obj.market_price < 600:
            reasons.append("low_price")

        if getattr(obj, "risk", 0) < 0.3:
            reasons.append("low_risk")

        if getattr(obj, "area_score", 0) > 7:
            reasons.append("good_area")

        obj.explanation = reasons

        return obj

