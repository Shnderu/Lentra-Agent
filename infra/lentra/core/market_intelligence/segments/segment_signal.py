from typing import Dict, Any


class SegmentSignalAdapter:
    """
    Adapter between Segment Market Intelligence
    and Decision Layer.

    Does NOT calculate market.
    Uses existing segment_market truth.
    """


    def build(
        self,
        segment_market: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(
            segment_market,
            dict
        ):
            segment_market = {}


        sample_size = segment_market.get(
            "sample_size",
            0
        )


        median_price = segment_market.get(
            "median_price",
            0
        )


        if sample_size >= 10:
            confidence = 1.0

        elif sample_size >= 5:
            confidence = 0.7

        elif sample_size >= 2:
            confidence = 0.4

        else:
            confidence = 0.1


        return {

            "confidence": confidence,

            "median_price":
                median_price,

            "sample_size":
                sample_size,

            "price_min":
                segment_market.get(
                    "price_min"
                ),

            "price_max":
                segment_market.get(
                    "price_max"
                ),

            "market_strength":
                (
                    "strong"
                    if confidence >= 0.7
                    else
                    "limited"
                ),

            "position":
                (
                    "known"
                    if sample_size > 0
                    else
                    "unknown"
                )

        }
