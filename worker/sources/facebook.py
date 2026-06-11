from .base import BaseSource

class FacebookSource(BaseSource):
    name = "facebook"

    def search(self, query: dict):
        city = query.get("city")

        # MOCK DATA (later: Graph API / scraping layer)
        return [
            {
                "title": f"FB Rental in {city}",
                "price": 600,
                "currency": "USD",
                "location": city,
                "source": "facebook",
                "url": "https://facebook.com/mock"
            }
        ]
