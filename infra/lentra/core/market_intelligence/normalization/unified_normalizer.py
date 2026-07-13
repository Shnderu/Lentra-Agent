from lentra.core.market_intelligence.normalization.listing_normalizer import (
    ListingNormalizer,
)


class UnifiedNormalizer:
    """
    SINGLE normalization entry point.

    Delegates to ListingNormalizer facade.
    """

    def __init__(self):
        self.normalizer = ListingNormalizer()

    def normalize(self, item: dict):
        normalized = self.normalizer.normalize(item)

        normalized["price"] = float(
            normalized.get("price") or 0
        )

        return normalized
