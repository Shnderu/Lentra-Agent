from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json


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

        self.storage_path = Path(
            "lentra/storage/market_snapshots/market_snapshots.json"
        )

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self._snapshots = self._load()


    def _load(self) -> list:

        if not self.storage_path.exists():

            return []

        try:

            with self.storage_path.open(
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            if isinstance(data, list):

                return data

        except Exception:

            pass


        return []


    def _persist(self) -> None:

        with self.storage_path.open(
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self._snapshots,
                f,
                ensure_ascii=False,
                indent=2
            )


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

        self._persist()

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
