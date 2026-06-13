from dataclasses import dataclass

@dataclass
class VietnamRentQuery:
    city: str = "Ho Chi Minh City"
    budget_min: int = 0
    budget_max: int = 1000
    rooms: int = 1
    furnished: bool = True
    district: str = None
    keywords: str = None
