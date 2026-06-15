from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class FavoritesStore:
    store: Dict[int, Set[int]] = field(default_factory=dict)

    def add(self, user_id: int, item_id: int):
        self.store.setdefault(user_id, set()).add(item_id)

    def list(self, user_id: int) -> Set[int]:
        return self.store.get(user_id, set())
