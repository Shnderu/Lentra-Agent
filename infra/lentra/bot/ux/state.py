from dataclasses import dataclass


@dataclass
class SearchState:
    query: str
    offset: int = 0
    limit: int = 5
