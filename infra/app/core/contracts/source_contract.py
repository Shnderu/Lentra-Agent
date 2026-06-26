from typing import List
from lentra.core.contracts.listing_dto import ListingDTO


class BaseRentSource:
    """
    Абстрактный контракт для всех источников аренды
    """

    def search(self, query: str) -> List[ListingDTO]:
        raise NotImplementedError
