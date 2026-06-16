from dataclasses import dataclass


@dataclass
class Event:
    type: str
    user_id: int
    payload: dict
