from typing import Dict, Any, List
import hashlib


class EntityResolver:
    """
    Dedup Intelligence V4

    Responsibility:
    - resolve duplicate clusters into property entities
    - create stable entity identifiers
    - aggregate linked listings

    Supports:
    - cluster contract
    - raw listings list compatibility
    """

    def resolve(
        self,
        cluster: Any
    ) -> Dict[str, Any]:

        # --------------------------------------------------
        # CONTRACT NORMALIZATION
        # --------------------------------------------------

        if isinstance(cluster, list):

            members = [
                item.get("id")
                for item in cluster
                if isinstance(item, dict)
            ]

            canonical = (
                members[0]
                if members
                else "unknown"
            )

        elif isinstance(cluster, dict):

            members = cluster.get(
                "members",
                []
            )

            canonical = cluster.get(
                "canonical_listing",
                "unknown"
            )

        else:

            members = []

            canonical = "unknown"


        entity_id = self._entity_id(
            canonical
        )


        confidence = self._confidence(
            len(members)
        )


        return {

            "entity_id": entity_id,

            "canonical_listing":
                canonical,

            "linked_listings":
                members,

            "confidence":
                confidence,

            "status":
                "entity_resolved"

        }


    def _entity_id(
        self,
        canonical: str
    ) -> str:

        digest = hashlib.sha256(
            str(canonical).encode(
                "utf-8"
            )
        ).hexdigest()[:12]

        return (
            "property_"
            + digest
        )


    def _confidence(
        self,
        count: int
    ) -> float:

        if count <= 1:
            return 0.0

        if count == 2:
            return 0.8

        return 0.95
