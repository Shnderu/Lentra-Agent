
from lentra.core.data_layer.sources.base import BaseSource


class FacebookSource(BaseSource):

    def fetch(self):
        # MVP stub (потом заменим на real scraping/API)
        return [
            {
                "title": "Studio near beach Da Nang",
                "price": 700,
                "currency": "USD",
                "location": "da nang",
                "raw": "fb_post_1"
            },
            {
                "title": "Modern apartment center",
                "price": 650,
                "currency": "USD",
                "location": "da nang",
                "raw": "fb_post_2"
            }
        ]
