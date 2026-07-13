from typing import List, Dict, Any

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


        prices = [

            item.get(
                "price"
            )

            for item in listings

            if item.get(
                "price"
            )

        ]


        if not prices:

            return {
                "market_price": 0,
                "average_price": 0,
                "sample_size": 0
            }


        average_price = sum(
            prices
        ) / len(
            prices
        )


        return {

            "market_price":
                round(
                    average_price,
                    2
                ),

            "average_price":
                round(
                    average_price,
                    2
                ),

            "sample_size":
                len(
                    prices
                ),

            "price_min":
                min(
                    prices
                ),

            "price_max":
                max(
                    prices
                )

        }



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

            "market_price":
                market_price,

            "pricing_score":
                pricing.get(
                    "score",
                    0.5
                ),

            "price_delta":
                pricing.get(
                    "delta",
                    0
                ),

            "price_deviation":
                pricing.get(
                    "deviation",
                    0
                )

        }
