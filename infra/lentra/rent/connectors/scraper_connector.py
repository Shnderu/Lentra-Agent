# ============================================================
# SCRAPER CONNECTOR V16.2
# ============================================================

from typing import Dict, Any, List
import asyncio
from lentra.rent.connectors.base import BaseConnector


class ScraperConnector(BaseConnector):
    name = "scraper"

    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.3)

        return [
            {
                "id": "sc_3001",
                "title": "Private landlord listing",
                "city": query.get("city"),
                "price": 480,
                "rooms": 1,
                "lat": 10.770,
                "lon": 106.705,
                "district": "District 2",
                "source": "scraper",
                "url": "https://source.example/listing/3001"
            }
        ]
