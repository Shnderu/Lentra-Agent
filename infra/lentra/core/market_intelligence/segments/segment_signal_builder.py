from typing import Dict, Any


class SegmentSignalBuilder:
    """
    Normalizes segment intelligence into canonical market signal.

    This is NOT a decision engine.

    Responsibility:
    convert segment market data into a stable contract
    consumed by Decision Layer and presentation layers.
    """


    def build(
        self,
        segment_key: str,
        segment_intelligence: Dict[str, Any],
        current_price: float
    ) -> Dict[str, Any]:

        if not isinstance(
            segment_intelligence,
            dict
        ):
            segment_intelligence = {}


        segments = segment_intelligence.get(
            "segments",
            {}
        )


        if not isinstance(
            segments,
            dict
        ):
            segments = {}


        segment = segments.get(
            segment_key,
            {}
        )


        if not isinstance(
            segment,
            dict
        ):
            segment = {}


        median_price = segment.get(
            "median_price",
            0
        )


        sample_size = segment.get(
            "samples",
            segment.get(
                "sample_size",
                0
            )
        )


        try:
            median_price = float(
                median_price
            )
        except Exception:
            median_price = 0


        try:
            current_price = float(
                current_price
            )
        except Exception:
            current_price = 0


        if median_price:

            delta = (
                current_price
                -
                median_price
            )

            delta_percent = round(
                (
                    delta
                    /
                    median_price
                )
                *
                100,
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

            position = (
                "below_segment_market"
            )

        elif delta_percent >= 10:

            position = (
                "above_segment_market"
            )

        else:

            position = (
                "within_segment_market"
            )


        return {

            "segment_key":
                segment_key,

            "median_price":
                median_price,

            "sample_size":
                sample_size,

            "status":
                segment.get(
                    "status",
                    "unknown"
                ),

            "segment_price_delta":
                delta,

            "segment_price_delta_percent":
                delta_percent,

            "position":
                position,

            "confidence":
                confidence

        }
