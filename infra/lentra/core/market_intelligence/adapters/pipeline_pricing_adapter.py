from statistics import median
from typing import List, Dict, Any

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine,
)


class PipelinePricingAdapter:
    """
    Data Layer pricing boundary.

    Converts:

        price_vnd

    into Market Intelligence:

        price

    Delegates pricing evaluation
    to PricingEngine.
    """

    def __init__(self):

        self.engine = PricingEngine()


    def _prepare_listing(
        self,
        item: Dict[str, Any]
    ) -> Dict[str, Any]:

        payload = {
            **item
        }

        if "price" not in payload:

            payload["price"] = payload.get(
                "price_vnd",
                0
            )

        return payload


    def build_market(
        self,
        clusters: list
    ) -> dict:

        listings = []


        for cluster in clusters:

            for item in cluster:

                listings.append(
                    self._prepare_listing(
                        item
                    )
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
                "median_price": 0,
                "sample_size": 0
            }


        market_price = median(
            prices
        )


        return {

            "market_price":
                market_price,

            "median_price":
                market_price,

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


        payload = self._prepare_listing(
            item
        )


        market_price = market_stats.get(
            "market_price",
            0
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


        deviation = pricing.get(
            "deviation",
            0
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

            # canonical search/API field
            "deviation_pct":
                deviation,

            # backward compatibility
            "price_deviation":
                deviation
        }
