from lentra.core.market_intelligence.engines.pricing_engine import PricingEngine
from lentra.core.market_intelligence.models.market_object import MarketObject


class MarketObjectPricingAdapter:
    """
    MVP bridge:

    MarketObject
        ->
    PricingEngine
        ->
    price intelligence
    """

    def __init__(self):
        self.engine = PricingEngine()

    def evaluate(
        self,
        market_object: MarketObject
    ) -> dict:

        payload = {
            "price": (
                market_object.listings[0].price
                if market_object.listings
                else 0
            ),
            "market_price": (
                market_object.market_price
                or 0
            )
        }

        return self.engine.evaluate(
            payload
        )
