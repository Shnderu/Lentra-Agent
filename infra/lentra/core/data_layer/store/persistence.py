from typing import Dict, Any, List
from copy import deepcopy


class PersistenceLayer:
    """
    VIETNAM LISTING STORE

    Features:
    - in-memory persistence (MVP)
    - upsert by id
    - history tracking
    """

    def __init__(self):
        self.current = {}   # id -> latest listing
        self.history = {}   # id -> list of versions

    def upsert(self, item: Dict[str, Any]) -> Dict[str, Any]:
        item_id = item.get("id")

        if not item_id:
            return item

        # store history
        if item_id not in self.history:
            self.history[item_id] = []

        if item_id in self.current:
            self.history[item_id].append(deepcopy(self.current[item_id]))

        # update current
        self.current[item_id] = deepcopy(item)

        return item

    def get(self, item_id: str) -> Dict[str, Any]:
        return self.current.get(item_id)

    def all(self) -> List[Dict[str, Any]]:
        return list(self.current.values())

    def get_history(self, item_id: str) -> List[Dict[str, Any]]:
        return self.history.get(item_id, [])
