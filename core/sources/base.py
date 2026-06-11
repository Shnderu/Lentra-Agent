from abc import ABC, abstractmethod
from typing import List
from core.domain import RentQuery, RentListing


class BaseSource(ABC):

    name: str

    @abstractmethod
    def search(self, query: RentQuery) -> List[RentListing]:
        pass
