from typing import Dict, Any, List
import statistics

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine
)


class PipelinePricingAdapter:
    """
    ARCH V2 CONTRACT

    Data Layer:
        price_vnd

    Market Intelligence:
        market_price
        pricing signals
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


        item["price"] = float(
            price or 0
        )


        return item



    def build_market(
        self,
        clusters: List[List[Dict[str, Any]]]
    ) -> Dict[str, Any]:

        segments = {}


        for cluster in clusters:

            for item in cluster:

                prepared = self._prepare_listing(
                    item
                )


                segment = prepared.get(
                    "segment_key",
                    "unknown"
                )


                if segment not in segments:

                    segments[segment] = []


                if prepared["price"] > 0:

                    segments[segment].append(
                        prepared["price"]
                    )


        result = {}


        for segment, prices in segments.items():

            result[segment] = {

                "market_price": statistics.median(
                    prices
                ) if prices else 0,

                "sample_size": len(
                    prices
                ),

                "price_min": min(
                    prices
                ) if prices else 0,

                "price_max": max(
                    prices
                ) if prices else 0

            }


        return result



    def _resolve_market(
        self,
        listing: Dict[str, Any],
        market_stats: Dict[str, Any]
    ) -> Dict[str, Any]:

        segment = listing.get(
            "segment_key",
            "unknown"
        )


        if segment in market_stats:

            return market_stats[segment]


        return {

            "market_price": 0,

            "sample_size": 0

        }



    def evaluate(
        self,
        listing: Dict[str, Any],
        market_stats: Dict[str, Any]
    ) -> Dict[str, Any]:

        payload = self._prepare_listing(
            listing
        )


        segment_market = self._resolve_market(
            payload,
            market_stats
        )


        payload["market_price"] = float(
            segment_market.get(
                "market_price",
                0
            )
        )


        return self.engine.run(
            payload
        )
