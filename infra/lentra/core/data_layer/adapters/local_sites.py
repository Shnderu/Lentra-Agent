from typing import List, Dict, Any
from lentra.core.data_layer.adapters.base import BaseAdapter


class LocalSitesAdapter(BaseAdapter):
    """
    Vietnam real estate portals (batdongsan, chotot, etc.)
    """

    def fetch(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "site_001",
                "source": "batdongsan",
                "source_url": "https://batdongsan.vn/listing/001",

                "title": "Villa in Hanoi Tay Ho",
                "description": "Luxury villa, lake view",

                "price": "30000000",
                "currency": "VND",

                "property_type": "villa",
                "size": "120",

                "location": "Hanoi, Tay Ho",

                "images": [],
                "contact": "agent@vnmail.com",
                "timestamp": "2026-06-26"
            }
        ]
