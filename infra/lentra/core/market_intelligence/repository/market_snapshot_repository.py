from typing import Dict, Any, Optional
from datetime import datetime


class MarketSnapshotRepository:
    """
    Repository for Market Intelligence market snapshots.

    Responsibility:

    - store calculated market truth snapshots
    - retrieve latest snapshot
    - provide persistence boundary

    No business logic here.
    """

    def __init__(self):

        self._snapshots = []


    def save(
        self,
        snapshot: Dict[str, Any]
    ) -> Dict[str, Any]:

        record = {

            "created_at": datetime.utcnow().isoformat(),

            **snapshot

        }

        self._snapshots.append(
            record
        )

        return record


    def latest(
        self,
        city: str
    ) -> Optional[Dict[str, Any]]:

        items = [

            item

            for item in self._snapshots

            if item.get(
                "city"
            ) == city

        ]


        if not items:

            return None


        return items[-1]


    def history(
        self,
        city: str
    ) -> list[Dict[str, Any]]:

        return [

            item

            for item in self._snapshots

            if item.get(
                "city"
            ) == city

        ]
