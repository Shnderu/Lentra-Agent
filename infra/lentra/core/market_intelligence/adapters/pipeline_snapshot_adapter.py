from typing import Dict, Any

from lentra.core.market_intelligence.snapshot.market_price_history import (
    MarketPriceHistory,
)


class PipelineSnapshotAdapter:
    """
    ARCH V2 CONTRACT BOUNDARY

    Data Layer:
        normalized listing

    Market Intelligence:
        snapshot history

    Responsibility:
        adapt pipeline payload into snapshot contract.
    """


    def __init__(self):

        self.engine = MarketPriceHistory()


    def update(
        self,
        snapshot: Dict[str, Any],
        item: Dict[str, Any],
    ) -> Dict[str, Any]:

        return self.engine.add_observation(
            snapshot,
            item,
        )


    def enrich(
        self,
        item: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Pipeline contract method.

        Creates/updates market snapshot
        for normalized listing.
        """

        snapshot = {
            "first_seen": None,
            "last_seen": None,
            "prices": [],
            "sources": [],
            "observations": 0,
        }

        return self.update(
            snapshot,
            item,
        )
