from typing import Dict, Any


class SegmentSignalAdapter:
    """
    Adapter between Segment Market Intelligence
    and Decision Layer.

    Does NOT calculate market.
    Converts segment truth into decision contract.
    """


    def build(
        self,
        price: float,
        segment_market: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(
            segment_market,
            dict
        ):
            segment_market = {}


        try:
            current_price = float(price)
        except Exception:
            current_price = 0


        sample_size = segment_market.get(
            "sample_size",
            segment_market.get(
                "samples",
                0
            )
        )


        prices = segment_market.get(
            "prices",
            []
        )


        median_price = segment_market.get(
            "median_price",
            0
        )


        if not median_price and prices:

            sorted_prices = sorted(
                prices
            )

            middle = len(sorted_prices) // 2

            if len(sorted_prices) % 2:

                median_price = sorted_prices[middle]

            else:

                median_price = (
                    sorted_prices[middle - 1]
                    +
                    sorted_prices[middle]
                ) / 2


        try:
            median_price = float(
                median_price
            )
        except Exception:
            median_price = 0


        if median_price:

            delta = (
                current_price
                -
                median_price
            )

            delta_percent = round(
                (
                    delta /
                    median_price
                ) * 100,
                2
            )

        else:

            delta = 0
            delta_percent = 0


        if sample_size >= 10:

            confidence = 1.0

        elif sample_size >= 5:

            confidence = 0.7

        elif sample_size >= 2:

            confidence = 0.4

        else:

            confidence = 0.1


        if delta_percent <= -10:

            position = "below_segment_market"

        elif delta_percent >= 10:

            position = "above_segment_market"

        else:

            position = "within_segment_market"


        return {

            "confidence":
                confidence,

            "median_price":
                median_price,

            "sample_size":
                sample_size,

            "price_min":
                min(prices)
                if prices
                else None,

            "price_max":
                max(prices)
                if prices
                else None,

            "segment_price_delta":
                delta,

            "segment_price_delta_percent":
                delta_percent,

            "position":
                position,

            "market_strength":
                (
                    "strong"
                    if confidence >= 0.7
                    else "limited"
                ),

            "status":
                segment_market.get(
                    "status",
                    "unknown"
                )

        }
