from typing import Dict, Any
from datetime import datetime


class ObjectMemory:

    """
    Dedup Intelligence V4

    Historical memory for normalized objects.
    """

    def __init__(self):

        self.objects = {}


    def update(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        object_id = listing.get(
            "id",
            "unknown"
        )

        now = datetime.utcnow().isoformat()

        if object_id not in self.objects:

            self.objects[object_id] = {

                "object_id": object_id,

                "first_seen": now,

                "last_seen": now,

                "repost_count": 1,

                "source_history": [
                    listing.get(
                        "source",
                        "unknown"
                    )
                ],

                "price_history": [
                    listing.get(
                        "price",
                        0
                    )
                ]

            }

        else:

            memory = self.objects[object_id]

            memory["last_seen"] = now

            memory["repost_count"] += 1


            source = listing.get(
                "source",
                "unknown"
            )

            if source not in memory["source_history"]:
                memory["source_history"].append(
                    source
                )


            price = listing.get(
                "price",
                0
            )

            if price not in memory["price_history"]:
                memory["price_history"].append(
                    price
                )


        return self.objects[object_id]
