from typing import Dict, Any, List
import statistics

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine
)


class PipelinePricingAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        price_vnd

    Market Intelligence:
        price
        market_price

    Market is calculated per segment_key.
    """

    def __init__(self):

        self.engine = PricingEngine()


    def _prepare_listing(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        item = {
            **listing
        }

        price = item.get(
            "price"
        )

        if price is None:

            price = item.get(
                "price_vnd"
            )

        if price is None:

            price = 0

        item["price"] = float(
            price
        )

        return item


    def build_market(
        self,
        clusters: List[List[Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Any]]:

        segments: Dict[str, List[float]] = {}

        for cluster in clusters:

            for item in cluster:

                prepared = self._prepare_listing(
                    item
                )

                if prepared["price"] <= 0:
                    continue

                segment = prepared.get(
                    "segment_key"
                ) or "unknown"

                segments.setdefault(
                    segment,
                    []
                ).append(
                    prepared["price"]
                )

        market = {}

        for segment, prices in segments.items():

            market[segment] = {

                "market_price": statistics.median(
                    prices
                ),

                "sample_size": len(
                    prices
                ),

                "price_min": min(
                    prices
                ),

                "price_max": max(
                    prices
                )

            }

        return market


    def evaluate(
        self,
        listing: Dict[str, Any],
        market_stats: Dict[str, Any]
    ) -> Dict[str, Any]:

        payload = self._prepare_listing(
            listing
        )

        market_price = market_stats.get(
            "market_price",
            0
        )

        if market_price is None:

            market_price = 0

        payload["market_price"] = float(
            market_price
        )

        return self.engine.run(
            payload
        )

