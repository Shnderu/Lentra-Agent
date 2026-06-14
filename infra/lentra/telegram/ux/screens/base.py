from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class UXButton:
    text: str
    callback_data: str


@dataclass
class UXScreen:
    """
    Base UX Screen contract
    """
    screen: str
    text: str
    cards: Optional[List[Dict[str, Any]]] = None
    buttons: Optional[List[UXButton]] = None

    def to_dict(self):
        return {
            "screen": self.screen,
            "text": self.text,
            "cards": self.cards or [],
            "buttons": [
                {
                    "text": b.text,
                    "callback_data": b.callback_data
                }
                for b in (self.buttons or [])
            ]
        }
