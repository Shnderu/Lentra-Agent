from abc import ABC, abstractmethod
from typing import List
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class RentProvider(ABC):

    @abstractmethod
    def search(self, context: SearchContext) -> List[RentSearchItem]:
        """
        Унифицированный контракт получения объявлений
        """
        pass
