from typing import List, Dict


class RentRepository:
    """
    Data access layer (MVP mock implementation).

    Later will be replaced with:
    - DB (PostgreSQL)
    - external APIs
    - scraping adapters
    """

    def fetch_listings(self, query: str, city: str | None = None) -> List[Dict]:
        # MOCK SOURCE DATA (raw layer)
        return [
            {
                "id": "1",
                "title": "Modern studio near center",
                "city": city or "Unknown",
                "price": 500,
                "currency": "USD",
                "score": 0.87,
            },
            {
                "id": "2",
                "title": "Cozy apartment with balcony",
                "city": city or "Unknown",
                "price": 650,
                "currency": "USD",
                "score": 0.81,
            },
            {
                "id": "3",
                "title": "Budget room for expats",
                "city": city or "Unknown",
                "price": 300,
                "currency": "USD",
                "score": 0.76,
            },
        ]
