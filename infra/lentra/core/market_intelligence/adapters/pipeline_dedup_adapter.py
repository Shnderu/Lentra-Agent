from typing import List, Dict, Any

from lentra.core.market_intelligence.engines.dedup_engine import (
    DedupEngine,
)


class PipelineDedupAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer contract:

        deduplicate(listings)
            ->
        {"clusters": [...]}

    Market Intelligence authority:

        DedupEngine
            |
            +--> DedupIndex V4
            +--> Entity Resolution
            +--> Object Memory
    """


    def __init__(self):

        self.engine = DedupEngine()



    def deduplicate(
        self,
        listings: List[Dict[str, Any]]
    ) -> Dict[str, Any]:


        clusters = []

        processed = set()


        evaluated = []


        for listing in listings:

            result = self.engine.evaluate(
                listing
            )

            evaluated.append(
                result
            )


        for item in evaluated:

            listing_id = item.get(
                "id"
            )


            if listing_id in processed:
                continue


            dedup = item.get(
                "dedup",
                {}
            )


            matches = dedup.get(
                "matches",
                []
            )


            cluster = [
                item
            ]


            cluster.extend(
                matches
            )


            for member in cluster:

                member_id = member.get(
                    "id"
                )

                if member_id:

                    processed.add(
                        member_id
                    )


            clusters.append(
                cluster
            )


        return {

            "clusters":
                clusters,

            "status":
                "ok"

        }
