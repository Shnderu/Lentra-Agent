from typing import Dict, Any, List


class DuplicateClusterEngine:
    """
    Dedup Intelligence V3

    Responsibility:
    - build duplicate clusters
    - choose canonical listing
    - aggregate sources
    """


    def build_cluster(
        self,
        listing: Dict[str, Any],
        matches: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        cluster_items = [
            listing
        ]

        cluster_items.extend(
            matches
        )


        canonical = self._select_canonical(
            cluster_items
        )


        sources = list(
            {
                item.get(
                    "source",
                    "unknown"
                )
                for item in cluster_items
            }
        )


        return {

            "cluster_id":
                self._cluster_id(
                    canonical
                ),

            "canonical_listing":
                canonical.get(
                    "id"
                ),

            "duplicate_count":
                max(
                    len(cluster_items) - 1,
                    0
                ),

            "sources":
                sources,

            "members":
                [
                    item.get(
                        "id"
                    )
                    for item in cluster_items
                ],

            "confidence":
                self._confidence(
                    len(cluster_items)
                )

        }


    def _select_canonical(
        self,
        items: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        return sorted(
            items,
            key=lambda x:
                (
                    x.get(
                        "source",
                        ""
                    ) == "agency",
                    x.get(
                        "description",
                        ""
                    ).__len__()
                ),
            reverse=True
        )[0]


    def _confidence(
        self,
        count: int
    ) -> float:

        if count <= 1:
            return 0.0

        if count == 2:
            return 0.75

        if count >= 3:
            return 0.9

        return 0.5


    def _cluster_id(
        self,
        canonical: Dict[str, Any]
    ) -> str:

        return (
            "cluster_"
            + str(
                canonical.get(
                    "id",
                    "unknown"
                )
            )
        )
