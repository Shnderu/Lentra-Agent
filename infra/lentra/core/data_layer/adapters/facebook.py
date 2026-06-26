from typing import List, Dict, Any
from lentra.core.data_layer.adapters.base import BaseAdapter


class FacebookAdapter(BaseAdapter):
    """
    Simulated Facebook Groups ingestion
    (real scraper will be plugged later)
    """

    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "fb_001",
                "source": "facebook",
                "source_url": "https://facebook.com/group/post/001",

                "title": "Nice studio in Da Nang near beach",
                "description": "Fully furnished, good internet",

                "price": "12000000",
                "currency": "VND",

                "property_type": "studio",
                "size": "35",

                "location": "Da Nang, Son Tra",

                "images": [],
                "contact": "+84xxxx",
                "timestamp": "2026-06-26"
            }
        ]
