from abc import ABC, abstractmethod
from core.domain import RentQuery, RentListing
from typing import List


class BaseProvider(ABC):
    name: str
    rate_limit: float = 1.0

    @abstractmethod
    def fetch(self, query: RentQuery) -> List[RentListing]:
        pass
