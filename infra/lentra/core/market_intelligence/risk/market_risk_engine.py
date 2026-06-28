
from lentra.core.market_intelligence.models.market_object import MarketObject


class MarketRiskEngine:

    def run(self, obj: MarketObject) -> MarketObject:

        risk = 0.5  # baseline

        # 1. Price anomaly
        if obj.price_deviation is not None:

            risk += abs(obj.price_deviation) * 0.3

        # 2. Listing count signal
        if obj.listing_count == 1:
            risk += 0.2

        elif obj.listing_count >= 4:
            risk -= 0.1

        # 3. Source diversity
        sources = len(obj.sources)

        if sources == 1:
            risk += 0.15

        elif sources >= 3:
            risk -= 0.1

        # clamp
        risk = max(0.0, min(1.0, risk))

        obj.risk = risk

        return obj
