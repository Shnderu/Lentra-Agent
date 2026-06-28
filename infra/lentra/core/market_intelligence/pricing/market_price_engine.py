
from statistics import median
from lentra.core.market_intelligence.models.market_object import MarketObject


class MarketPriceEngine:

    def run(self, obj: MarketObject) -> MarketObject:

        prices = [
            l.price
            for l in obj.listings
            if l.price is not None
        ]

        if not prices:

            obj.market_price = None
            obj.median_price = None
            obj.price_deviation = None

            return obj

        obj.market_price = sum(prices) / len(prices)
        obj.median_price = median(prices)

        # deviation = relative spread from median
        if obj.median_price > 0:

            obj.price_deviation = (
                obj.market_price - obj.median_price
            ) / obj.median_price

        else:

            obj.price_deviation = 0.0

        return obj
