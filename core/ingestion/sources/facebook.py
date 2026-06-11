from core.ingestion.sources.base import BaseSource


class FacebookSource(BaseSource):
    name = "facebook"

    def search(self, payload: dict):
        city = payload.get("city", "")
        budget = payload.get("budget", 0)

        return [
            {
                "title": f"FB Rental in {city}",
                "price": budget * 0.6,
                "currency": "USD",
                "location": city,
                "source": self.name,
                "url": "https://facebook.com/mock"
            }
        ]
