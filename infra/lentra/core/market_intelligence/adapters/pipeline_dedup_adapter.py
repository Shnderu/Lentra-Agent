from typing import List, Dict, Any

from lentra.core.market_intelligence.dedup.dedup_index import (
    DedupIndex
)


class PipelineDedupAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        deduplicate(listings)
            ->
        {"clusters": [...]}

    Market Intelligence:
        DedupIndex V4
            ->
        entity resolution
        duplicate intelligence
    """

    def __init__(self):
        self.index = DedupIndex()


    def deduplicate(
        self,
        listings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        clusters = []

        processed = set()


        for listing in listings:

            listing_id = listing.get(
                "id"
            )

            if listing_id in processed:
                continue


            result = self.index.analyze(
                listing
            )


            matches = result.get(
                "matches",
                []
            )


            cluster_items = [
                listing
            ]

            cluster_items.extend(
                matches
            )


            for item in cluster_items:

                item_id = item.get(
                    "id"
                )

                if item_id:
                    processed.add(
                        item_id
                    )


            clusters.append(
                cluster_items
            )


        return {
            "clusters": clusters,
            "status": "ok"
        }
