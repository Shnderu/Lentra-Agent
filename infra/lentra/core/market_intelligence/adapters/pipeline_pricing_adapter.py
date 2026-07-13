from lentra.core.market.vietnam_market import build_market_index

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine,
)


class PipelinePricingAdapter:
    """
    Data Layer pricing boundary.

    Keeps ingestion pipeline contract:

        build_market()
        evaluate()

    while routing intelligence into
    Market Intelligence PricingEngine.
    """


    def __init__(self):

        self.engine = PricingEngine()



    def build_market(
        self,
        clusters: list
    ) -> dict:

        listings = []

        for cluster in clusters:

            listings.extend(
                cluster
            )


        return build_market_index(
            listings
        )



    def evaluate(
        self,
        item: dict,
        market_stats: dict
    ) -> dict:

        payload = {
            **item
        }


        market_price = (
            market_stats.get(
                "market_price"
            )
            or market_stats.get(
                "average_price"
            )
            or market_stats.get(
                "avg"
            )
            or 0
        )


        payload["market_price"] = market_price


        result = self.engine.evaluate(
            payload,
            {
                "market_stats": market_stats
            }
        )


        pricing = result.get(
            "pricing",
            {}
        )


        return {
            "market_price": market_price,

            "pricing_score": pricing.get(
                "score",
                0.5
            ),

            "price_delta": pricing.get(
                "delta",
                0
            ),

            "price_deviation": pricing.get(
                "deviation",
                0
            )
        }
