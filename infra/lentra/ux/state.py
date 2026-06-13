from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class UserState:
    user_id: Optional[int] = None
    last_intent: Optional[str] = None
    last_scenario: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


STATE_CACHE = {}


def get_state(user_id: int) -> UserState:
    if user_id not in STATE_CACHE:
        STATE_CACHE[user_id] = UserState(user_id=user_id)
    return STATE_CACHE[user_id]


def update_state(user_id: int, **kwargs):
    state = get_state(user_id)
    for k, v in kwargs.items():
        setattr(state, k, v)
    return state
