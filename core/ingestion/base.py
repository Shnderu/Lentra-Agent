from abc import ABC, abstractmethod
from typing import List
from core.domain import RentQuery, RentListing


class BaseIngestionSource(ABC):
    name: str

    @abstractmethod
    def fetch(self, query: RentQuery) -> List[RentListing]:
        pass
