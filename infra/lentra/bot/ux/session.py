from dataclasses import dataclass


@dataclass
class UserSession:
    query: str = ""
    page: int = 0
    filters: dict = None

    def __post_init__(self):
        if self.filters is None:
            self.filters = {}
