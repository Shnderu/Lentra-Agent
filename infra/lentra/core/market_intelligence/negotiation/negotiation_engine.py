
from lentra.core.market_intelligence.models.market_object import MarketObject


class NegotiationEngine:

    def run(self, obj: MarketObject) -> MarketObject:

        # default strategy
        strategy = "low_room_for_negotiation"
        target_discount = 0.03

        # risk-based adjustment
        if obj.risk > 0.7:

            strategy = "high_room_for_negotiation"
            target_discount = 0.08

        elif obj.risk < 0.3:

            strategy = "firm_price"
            target_discount = 0.01

        # price deviation influence
        if obj.price_deviation:

            if obj.price_deviation > 0.1:

                target_discount += 0.03

            elif obj.price_deviation < -0.1:

                target_discount -= 0.01

        # area quality influence
        if obj.area_score:

            if obj.area_score > 7:

                target_discount -= 0.01

            elif obj.area_score < 4:

                target_discount += 0.02

        # clamp
        target_discount = max(0.01, min(0.15, target_discount))

        obj.negotiation = {
            "strategy": strategy,
            "target_discount": round(target_discount, 3)
        }

        return obj
