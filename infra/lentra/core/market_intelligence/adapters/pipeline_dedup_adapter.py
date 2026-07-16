from typing import List, Dict, Any
import hashlib


from lentra.core.market_intelligence.dedup.dedup_index import (
    DedupIndex
)


class PipelineDedupAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Dedup pipeline adapter.

    Flow:

    normalize
        |
    fingerprint
        |
    register batch
        |
    analyze duplicates
        |
    entity resolution
    """


    def __init__(self):

        self.index = DedupIndex()



    def _build_fingerprint(
        self,
        listing: Dict[str, Any]
    ) -> str:

        source = "|".join(

            [

                str(
                    listing.get(
                        "title",
                        ""
                    )
                ),

                str(
                    listing.get(
                        "city",
                        ""
                    )
                ),

                str(
                    listing.get(
                        "type",
                        ""
                    )
                ),

                str(
                    listing.get(
                        "description",
                        ""
                    )
                )

            ]

        )


        return hashlib.sha256(
            source.encode(
                "utf-8"
            )
        ).hexdigest()[:16]



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

            item["fingerprint"] = self._build_fingerprint(
                item
            )


        return item



    def deduplicate(
        self,
        listings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:


        prepared = [

            self._prepare_listing(
                item
            )

            for item in listings

        ]



        for item in prepared:

            self.index.register(
                item
            )



        clusters = []

        assigned = set()



        for listing in prepared:


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


            cluster = [

                listing

            ]


            assigned.add(
                listing_id
            )


            for match in matches:

                match_id = match.get(
                    "id"
                )


                if match_id and match_id not in assigned:

                    cluster.append(
                        match
                    )

                    assigned.add(
                        match_id
                    )



            clusters.append(
                cluster
            )



        return {

            "clusters": clusters,

            "status": "ok"

        }
