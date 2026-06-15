from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

from lentra.bot.events.types.base import Event


@dataclass
class SearchEvent(Event):
    pass


@dataclass
class ItemViewedEvent(Event):
    pass


@dataclass
class FilterAppliedEvent(Event):
    pass


def create_event(event_type: str, user_id: int, payload: Dict[str, Any]) -> Event:

    return Event(
        type=event_type,
        user_id=user_id,
        payload=payload,
        timestamp=datetime.utcnow()
    )
