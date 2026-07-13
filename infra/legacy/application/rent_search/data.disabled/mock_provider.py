from typing import List, Dict, Any
from .provider import RentDataProvider


class MockRentDataProvider(RentDataProvider):
    def fetch(self, query: str) -> List[Dict[str, Any]]:
        return [
            {
                "title": f"[MOCK] Apartment for: {query}",
                "price": "500$",
                "city": "Hanoi",
                "meta": {"source": "mock"}
            }
        ]
