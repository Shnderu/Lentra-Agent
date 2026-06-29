from lentra.core.ingestion.normalizers.listing_normalizer import normalize as ingestion_normalize


class UnifiedNormalizer:
    """
    SINGLE normalization entry point.
    """

    def normalize(self, item: dict):
        # ingestion normalization (primary truth)
        item = ingestion_normalize(item)

        # minimal safety cleanup
        item["price"] = float(item.get("price") or 0)

        return item
