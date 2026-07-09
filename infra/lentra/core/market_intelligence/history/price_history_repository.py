from typing import Dict, Any, List, Optional

from lentra.core.market_intelligence.history.price_observation import (
    PriceObservation
)


class PriceHistoryRepository:
    """
    Repository boundary for price history.

    Current storage:
    in-memory.

    Contract allows future replacement:
    JSON/Postgres/Event storage.
    """

    def __init__(self):

        self._events: List[Dict[str, Any]] = []


    def save(
        self,
        observation: PriceObservation
    ) -> Dict[str, Any]:

        record = observation.to_dict()

        self._events.append(
            record
        )

        return record


    def get_listing_history(
        self,
        listing_id: str
    ) -> List[Dict[str, Any]]:

        return [
            item
            for item in self._events
            if item.get("listing_id") == listing_id
        ]


    def get_latest_price(
        self,
        listing_id: str
    ) -> Optional[Dict[str, Any]]:

        history = self.get_listing_history(
            listing_id
        )

        if not history:
            return None

        return history[-1]


    def get_city_history(
        self,
        city: str
    ) -> List[Dict[str, Any]]:

        return [
            item
            for item in self._events
            if item.get("city") == city
        ]
