from typing import List, Dict, Any

from lentra.core.market_intelligence.dedup.dedup_index import (
    DedupIndex
)


class PipelineDedupAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        price_vnd

    Market Intelligence:
        price

    Adapter responsibility:
        convert Data Layer contract
        into Market Intelligence contract.
    """

    def __init__(self):

        self.index = DedupIndex()


    def _prepare_listing(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        item = {
            **listing
        }

        if "price" not in item:

            item["price"] = item.get(
                "price_vnd",
                0
            )

        return item


    def deduplicate(
        self,
        listings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        clusters = []

        assigned = set()


        prepared_listings = [

            self._prepare_listing(
                listing
            )

            for listing in listings
        ]


        for listing in prepared_listings:

            listing_id = listing.get(
                "id"
            )

            if not listing_id:
                continue


            if listing_id in assigned:
                continue


            result = self.index.analyze(
                listing
            )


            matches = result.get(
                "matches",
                []
            )


            cluster_items = []

            cluster_ids = set()


            def add_item(item):

                item = self._prepare_listing(
                    item
                )

                item_id = item.get(
                    "id"
                )

                if not item_id:
                    return


                if item_id in cluster_ids:
                    return


                cluster_ids.add(
                    item_id
                )

                cluster_items.append(
                    item
                )


            add_item(
                listing
            )


            for match in matches:

                add_item(
                    match
                )


            for item in cluster_items:

                item_id = item.get(
                    "id"
                )

                if item_id:

                    assigned.add(
                        item_id
                    )


            clusters.append(
                cluster_items
            )


        return {
            "clusters": clusters,
            "status": "ok"
        }
