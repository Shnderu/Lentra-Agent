

from lentra.core.ingestion.sources.facebook import FacebookSource
from lentra.core.ingestion.normalizers.listing_normalizer import normalize

from lentra.core.market_intelligence.dedup.dedup_v2 import (
    is_duplicate,
    register_signature
)

from lentra.api.search.search_api import SearchAPI


class IngestionEngine:

    def __init__(self):
        self.sources = [
            FacebookSource()
        ]

        self.seen = set()
        self.api = SearchAPI()

    def run(self):

        all_listings = []

        for source in self.sources:
            raw_items = source.fetch()

            for raw in raw_items:

                listing = normalize(raw)

                if is_duplicate(self.seen, listing):
                    continue

                self.seen = register_signature(self.seen, listing)

                result = self.api.search(listing)

                all_listings.append(result)

        return all_listings
