from typing import Dict, Any, List

from lentra.core.market_intelligence.dedup.cluster_engine import (
    DuplicateClusterEngine
)

from lentra.core.market_intelligence.dedup.similarity import (
    SimilarityEngine
)

from lentra.core.market_intelligence.dedup.object_memory import (
    ObjectMemory
)


class DedupIndex:
    """
    Dedup Intelligence V4

    Responsibilities:
    - fingerprint index
    - similarity matching
    - duplicate clustering
    - historical object memory
    """


    def __init__(self):

        self.index = {}

        self.similarity = SimilarityEngine()

        self.cluster_engine = DuplicateClusterEngine()

        self.memory = ObjectMemory()



    def register(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        fingerprint = listing.get(
            "fingerprint"
        )


        if not fingerprint:

            return {
                "status": "error",
                "reason": "missing_fingerprint"
            }


        self.index.setdefault(
            fingerprint,
            []
        )


        if listing not in self.index[fingerprint]:

            self.index[fingerprint].append(
                listing
            )


        return {
            "status": "registered",
            "fingerprint": fingerprint
        }



    def search(
        self,
        listing: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        matches = []


        for items in self.index.values():

            for item in items:

                if item.get("id") == listing.get("id"):
                    continue


                score = self.similarity.compare(
                    listing,
                    item
                )


                if score >= 0.7:

                    matches.append(
                        {
                            **item,
                            "similarity": score
                        }
                    )


        return matches



    def analyze(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        matches = self.search(
            listing
        )


        cluster = self.cluster_engine.build_cluster(
            listing,
            matches
        )


        memory = self.memory.update(
            listing
        )


        return {

            "duplicates":
                cluster.get(
                    "duplicate_count",
                    0
                ),

            "confidence":
                cluster.get(
                    "confidence",
                    0.0
                ),

            "sources":
                cluster.get(
                    "sources",
                    []
                ),

            "canonical_listing":
                cluster.get(
                    "canonical_listing"
                ),

            "cluster":
                cluster,

            "matches":
                matches,

            "object_memory":
                memory,

            "status":
                "memory_ready"

        }
