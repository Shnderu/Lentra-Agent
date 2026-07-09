from typing import Dict, Any


class ListingNormalizer:
    """
    Converts raw source listing into canonical listing format.

    Keeps all intelligence-required fields:
    - pricing
    - risk
    - dedup
    - area
    """

    def normalize(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        return {
            "id": listing.get(
                "id",
                ""
            ),

            "title": listing.get(
                "title",
                ""
            ),

            "description": listing.get(
                "description",
                ""
            ),

            "price": float(
                listing.get(
                    "price",
                    0
                )
                or 0
            ),

            "market_price": (
                float(
                    listing.get(
                        "market_price"
                    )
                )
                if listing.get(
                    "market_price"
                ) is not None
                else None
            ),

            "location": listing.get(
                "location",
                ""
            ),

            "city": listing.get(
                "city",
                "da_nang"
            ),

            "source": listing.get(
                "source",
                "unknown"
            ),

            "currency": listing.get(
                "currency",
                "USD"
            ),

            "url": listing.get(
                "url",
                ""
            ),

            "photos": listing.get(
                "photos",
                []
            ),

            "type": listing.get(
                "type",
                "apartment"
            ),

            "metadata": listing.get(
                "metadata",
                {}
            ),

            "relevance_score": listing.get(
                "relevance_score",
                0
            ),
        }
