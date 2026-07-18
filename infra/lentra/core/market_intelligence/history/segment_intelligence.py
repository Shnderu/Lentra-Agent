from typing import List, Dict, Any
from statistics import median


class SegmentIntelligence:
    """
    Segment level market intelligence.

    Uses canonical segment_key from normalization layer.

    Fallback:
    legacy area based segmentation.
    """


    def analyze(
        self,
        observations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        segments: Dict[str, List[float]] = {}


        for item in observations:

            segment = item.get(
                "segment_key"
            )


            if not segment:

                area = item.get(
                    "area"
                )

                if isinstance(area, dict):

                    segment = area.get(
                        "segment",
                        "unknown"
                    )

                else:

                    segment = (
                        area
                        or "unknown"
                    )


            price = item.get(
                "price"
            )


            if price is None:
                continue


            if segment not in segments:

                segments[segment] = []


            segments[segment].append(
                float(price)
            )


        result = {}


        for segment, prices in segments.items():

            median_price = median(
                prices
            )


            if len(prices) <= 1:

                status = "insufficient_data"

            elif median_price >= 700:

                status = "premium"

            elif median_price <= 500:

                status = "budget"

            else:

                status = "standard"


            result[segment] = {

                "median_price": median_price,

                "samples": len(prices),

                "status": status,

                "prices": prices

            }


        return {

            "city": (
                observations[0].get(
                    "city",
                    "unknown"
                )
                if observations
                else "unknown"
            ),

            "segments": result

        }
