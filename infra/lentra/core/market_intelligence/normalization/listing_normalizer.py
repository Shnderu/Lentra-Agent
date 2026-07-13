from typing import Dict, Any

from lentra.core.data_layer.normalization.engine import (
    NormalizationEngine,
)


class ListingNormalizer:
    """
    Compatibility facade.

    Canonical normalization lives in:
        core.data_layer.normalization.engine.NormalizationEngine

    This class MUST NOT own normalization logic.

    Responsibility:
    - delegate to Data Layer
    - keep temporary legacy fields
    required by existing intelligence pipeline
    """

    def __init__(self):

        self.engine = NormalizationEngine()


    def normalize(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:


        normalized = self.engine.normalize(
            listing
        )


        price_vnd = normalized.get(
            "price_vnd"
        )


        # Temporary compatibility contract.
        # Canonical field is price_vnd.
        # price exists only until full pipeline migration.

        normalized["price"] = (
            float(price_vnd)
            if price_vnd is not None
            else 0.0
        )


        normalized["market_price"] = (
            float(price_vnd)
            if price_vnd is not None
            else 0.0
        )


        normalized["currency"] = "VND"


        normalized["city"] = (
            listing.get(
                "city",
                "da_nang"
            )
        )


        normalized["type"] = (
            listing.get(
                "type",
                "apartment"
            )
        )


        normalized["url"] = (
            listing.get(
                "url",
                ""
            )
        )


        normalized["photos"] = (
            listing.get(
                "photos",
                []
            )
        )


        normalized["metadata"] = (
            listing.get(
                "metadata",
                {}
            )
        )


        normalized["relevance_score"] = (
            listing.get(
                "relevance_score",
                0
            )
        )


        return normalized
