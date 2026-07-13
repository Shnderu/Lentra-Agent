from typing import List, Dict, Any

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine,
)


class PipelinePricingAdapter:
    """
    Data Layer pricing boundary.

    Responsibility:

        clusters
            ->
        market statistics
            ->
        PricingEngine interpretation

    IMPORTANT:
    Market truth ownership belongs to MarketService.
    This adapter only prepares pricing context
    for compatibility with the ingestion pipeline.

    Currency contract:
        primary: price_vnd
        legacy fallback: price
    """

    def __init__(self):

        self.engine = PricingEngine()


    def _get_price(self, item: dict):

        return (
            item.get("price_vnd")
            if item.get("price_vnd") is not None
            else item.get("price")
        )


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
            self._get_price(item)
            for item in listings
            if self._get_price(item) is not None
        ]


        if not prices:

            return {
                "market_price_vnd": 0,
                "average_price_vnd": 0,
                "sample_size": 0
            }


        average_price = sum(
            prices
        ) / len(
            prices
        )


        return {

            "market_price_vnd":
                round(
                    average_price,
                    2
                ),

            "average_price_vnd":
                round(
                    average_price,
                    2
                ),

            # backward compatibility
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
                "market_price_vnd"
            )

            or market_stats.get(
                "market_price"
            )

            or market_stats.get(
                "average_price_vnd"
            )

            or 0

        )


        payload["market_price_vnd"] = market_price

        # keep compatibility for PricingEngine
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

            "market_price_vnd":
                market_price,

            # compatibility field
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
