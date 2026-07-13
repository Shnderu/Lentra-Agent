from statistics import median
from typing import Dict, Any


from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine,
)


class PipelinePricingAdapter:
    """
    Data Layer pricing boundary.

    Market segmentation V1:

    market bucket:
        city + property_type

    Example:

        Da Nang + studio
        Da Nang + apartment

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


    def _market_key(
        self,
        item: Dict[str, Any]
    ) -> str:

        city = (
            item.get("location", {})
            .get("city")
            or "unknown"
        ).lower()

        property_type = (
            item.get("property_type")
            or "unknown"
        ).lower()

        return f"{city}:{property_type}"


    def build_market(
        self,
        clusters: list
    ) -> dict:

        buckets = {}


        for cluster in clusters:

            for item in cluster:

                payload = self._prepare_listing(
                    item
                )

                key = self._market_key(
                    payload
                )

                buckets.setdefault(
                    key,
                    []
                ).append(
                    payload.get(
                        "price"
                    )
                )


        markets = {}


        for key, prices in buckets.items():

            prices = [
                p for p in prices
                if p
            ]

            if not prices:
                continue

            markets[key] = {
                "market_price": median(prices),
                "sample_size": len(prices),
                "price_min": min(prices),
                "price_max": max(prices)
            }


        return markets


    def evaluate(
        self,
        item: dict,
        market_stats: dict
    ) -> dict:


        payload = self._prepare_listing(
            item
        )


        key = self._market_key(
            payload
        )


        market = market_stats.get(
            key,
            {}
        )


        market_price = market.get(
            "market_price",
            0
        )


        payload["market_price"] = market_price


        result = self.engine.evaluate(
            payload,
            {
                "market_stats": market
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

            "market_price": market_price,

            "pricing_score": pricing.get(
                "score",
                0.5
            ),

            "price_delta": pricing.get(
                "delta",
                0
            ),

            "deviation_pct": deviation,

            "price_deviation": deviation,

            "market_segment": key
        }
