from core.ingestion.sources.base import BaseSource


class FaswazSource(BaseSource):
    name = "faswaz"

    def search(self, payload: dict):
        city = payload.get("city", "")
        budget = payload.get("budget", 0)

        return [
            {
                "title": f"Faswaz Apartment in {city}",
                "price": budget * 0.85,
                "currency": "USD",
                "location": city,
                "source": self.name,
                "url": "https://faswaz.com/mock"
            }
        ]
