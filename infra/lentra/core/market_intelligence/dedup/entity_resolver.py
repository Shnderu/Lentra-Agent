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
    - cluster dict contract
    - legacy list cluster format
    """


    def resolve(
        self,
        cluster
    ) -> Dict[str, Any]:

        members = []
        canonical = "unknown"


        # ---------------------------------
        # Normalize cluster input
        # ---------------------------------

        if isinstance(cluster, dict):

            members = cluster.get(
                "members",
                []
            )

            canonical = cluster.get(
                "canonical_listing",
                "unknown"
            )


        elif isinstance(cluster, list):

            members = cluster

            if members:

                canonical = (
                    members[0].get("id")
                    or "unknown"
                )


        # ---------------------------------
        # Build entity
        # ---------------------------------

        linked_ids = []

        for item in members:

            if isinstance(item, dict):

                linked_ids.append(
                    item.get(
                        "id",
                        "unknown"
                    )
                )

            else:

                linked_ids.append(
                    str(item)
                )


        entity_id = self._entity_id(
            canonical
        )

        confidence = self._confidence(
            len(linked_ids)
        )


        return {

            "entity_id": entity_id,

            "canonical_listing":
                canonical,

            "linked_listings":
                linked_ids,

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
            canonical.encode(
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
