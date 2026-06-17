from typing import List
from app.core.contracts.listing_dto import ListingDTO


class BaseRentSource:
    """
    Абстрактный контракт для всех источников аренды
    """

    def search(self, query: str) -> List[ListingDTO]:
        raise NotImplementedError
