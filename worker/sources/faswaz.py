from .base import BaseSource

class FaswazSource(BaseSource):
    name = "faswaz"

    def search(self, query: dict):
        city = query.get("city")

        # MOCK (позже заменится на real scraping/API)
        return [
            {
                "title": f"Faswaz Apartment in {city}",
                "price": 850,
                "currency": "USD",
                "location": city,
                "source": "faswaz",
                "url": "https://faswaz.com/mock"
            }
        ]
