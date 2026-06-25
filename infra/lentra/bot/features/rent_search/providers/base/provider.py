from abc import ABC, abstractmethod
from typing import List

from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class RentProvider(ABC):

    @abstractmethod
    async def search(self, context: SearchContext) -> List[RentSearchItem]:
        """
        Async contract for all providers
        """
        pass
