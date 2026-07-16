from typing import Dict, Any

from lentra.core.market_intelligence.snapshot.market_price_history import (
    MarketPriceHistory,
)


class PipelineSnapshotAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        normalized listing + dedup object memory

    Market Intelligence:
        snapshot history

    Responsibility:
        adapt object memory into market snapshot contract.
    """


    def __init__(self):

        self.engine = MarketPriceHistory()



    def update(
        self,
        snapshot: Dict[str, Any],
        item: Dict[str, Any],
    ) -> Dict[str, Any]:

        contract = {

            "object_id": snapshot.get(
                "object_id"
            ),

            "first_seen": snapshot.get(
                "first_seen"
            ),

            "last_seen": snapshot.get(
                "last_seen"
            ),

            "repost_count": snapshot.get(
                "repost_count",
                0
            ),

            "source_history": snapshot.get(
                "source_history",
                []
            ),

            "price_history": self._normalize_price_history(
                snapshot
            ),
        }


        return self.engine.add_observation(
            contract,
            item,
        )



    def _normalize_price_history(
        self,
        snapshot: Dict[str, Any],
    ):

        history = snapshot.get(
            "price_history",
            []
        )


        normalized = []


        for entry in history:

            if isinstance(
                entry,
                dict
            ):
                normalized.append(
                    entry
                )


        return normalized



    def enrich(
        self,
        item: Dict[str, Any],
        object_memory: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        snapshot = object_memory or {

            "object_id": item.get(
                "id"
            ),

            "first_seen": None,

            "last_seen": None,

            "repost_count": 0,

            "source_history": [],

            "price_history": [],
        }


        return self.update(
            snapshot,
            item,
        )
