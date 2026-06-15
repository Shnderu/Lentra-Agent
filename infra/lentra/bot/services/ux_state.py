from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class SearchState:
    query: str
    offset: int = 0
    limit: int = 5
    budget_max: float = 10
    pool: Optional[bool] = None
    sea_view: Optional[bool] = None


class UXStateManager:
    def __init__(self):
        self._state: Dict[int, SearchState] = {}

    def get(self, user_id: int) -> Optional[SearchState]:
        return self._state.get(user_id)

    def set(self, user_id: int, state: SearchState):
        self._state[user_id] = state

    def reset(self, user_id: int):
        if user_id in self._state:
            del self._state[user_id]


ux_state = UXStateManager()
