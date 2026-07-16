from typing import List, Dict, Any

from lentra.core.market_intelligence.dedup.dedup_index import (
    DedupIndex
)

from lentra.core.market_intelligence.engines.dedup_engine import (
    DedupEngine
)


class PipelineDedupAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Responsibility:
    - prepare listings for Dedup Intelligence
    - generate stable fingerprints
    - build duplicate clusters
    - expose entity metadata

    Compatibility:
    - keeps legacy clusters list format
    - adds cluster_metadata
    """

    def __init__(self):

        self.index = DedupIndex()

        self.engine = DedupEngine()


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


        if not item.get(
            "fingerprint"
        ):

            item["fingerprint"] = self.engine.build_fingerprint(
                item
            )


        return item


    def deduplicate(
        self,
        listings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        clusters = []

        cluster_metadata = []

        assigned = set()


        prepared_listings = [

            self._prepare_listing(
                listing
            )

            for listing in listings

        ]


        for listing in prepared_listings:

            self.index.register(
                listing
            )


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


            def add_item(
                item
            ):

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


            cluster_metadata.append(
                {
                    "entity": result.get(
                        "entity"
                    ),

                    "cluster": result.get(
                        "cluster"
                    ),

                    "object_memory": result.get(
                        "object_memory"
                    )
                }
            )


        return {

            "clusters": clusters,

            "cluster_metadata": cluster_metadata,

            "status": "ok"

        }
