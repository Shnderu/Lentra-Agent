from typing import Protocol, Dict, Any


class BaseEngine(Protocol):

    def process(self, listing: dict) -> dict:
        ...
