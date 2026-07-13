from abc import ABC, abstractmethod
from typing import List

from lentra.application.rent_search.dto.search_context import SearchContext
from lentra.application.rent_search.contracts.rent_item import RentSearchItem


class RentProvider(ABC):

    @abstractmethod
    async def search(self, context: SearchContext) -> List[RentSearchItem]:
        """
        Async contract for all providers
        """
        pass
