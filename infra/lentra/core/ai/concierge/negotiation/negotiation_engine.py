

class NegotiationEngine:

    def negotiate(self, listing_price: float, market_price: float, risk: float, area_score: float):

        deviation = (listing_price - market_price) / max(market_price, 1)

        # base strategy
        if risk > 0.75:
            strategy = "aggressive_lowball"
            target_discount = 0.15

        elif deviation > 0.2:
            strategy = "value_correction_offer"
            target_discount = 0.1

        elif area_score > 8:
            strategy = "soft_negotiation"
            target_discount = 0.03

        else:
            strategy = "minimal_negotiation"
            target_discount = 0.02

        target_price = listing_price * (1 - target_discount)

        arguments = self._build_arguments(deviation, risk, area_score)

        return {
            "strategy": strategy,
            "target_price": round(target_price, 2),
            "target_discount": round(target_discount, 3),
            "arguments": arguments
        }


    def _build_arguments(self, deviation, risk, area_score):

        args = []

        if deviation > 0.15:
            args.append("market_overpriced_signal")

        if risk > 0.7:
            args.append("risk_based_pressure")

        if area_score < 6:
            args.append("location_discount_leverage")

        return args
