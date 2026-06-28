
from lentra.core.market_intelligence.models.market_object import MarketObject


class VerdictEngine:

    def run(self, obj: MarketObject) -> MarketObject:

        score = 0.5

        # risk impact
        score -= obj.risk * 0.4

        # area impact
        if obj.area_score:

            score += (obj.area_score - 5) * 0.05

        # price deviation impact
        if obj.price_deviation:

            score -= abs(obj.price_deviation) * 0.3

        # negotiation impact
        if obj.negotiation:

            discount = obj.negotiation.get("target_discount", 0.03)

            score += discount * 0.2

        # clamp
        score = max(0.0, min(1.0, score))

        # map to verdict
        if score >= 0.75:

            verdict = "strong_buy"

        elif score >= 0.6:

            verdict = "good_deal"

        elif score >= 0.4:

            verdict = "neutral"

        elif score >= 0.25:

            verdict = "overpriced"

        else:

            verdict = "avoid"

        obj.verdict = verdict

        obj.confidence = round(score, 3)

        return obj
