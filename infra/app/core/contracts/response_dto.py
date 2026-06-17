from dataclasses import dataclass
from typing import List
from app.core.contracts.listing_dto import ListingDTO


@dataclass
class RentResponseDTO:
    """
    Финальный формат ответа системы (для UI/API)
    """

    query: str
    listings: List[ListingDTO]
    total: int
