# ============================================================
# LOCAL MARKET CONNECTOR V16.2
# ============================================================

from typing import Dict, Any, List
import asyncio
from lentra.rent.connectors.base import BaseConnector


class LocalMarketConnector(BaseConnector):
    name = "local_board"

    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.3)

        return [
            {
                "id": "lm_2001",
                "title": "Cheap apartment for expats",
                "city": query.get("city"),
                "price": 400,
                "rooms": 2,
                "lat": 10.782,
                "lon": 106.695,
                "district": "District 3",
                "source": "local_board",
                "url": "https://local.example/listing/2001"
            }
        ]
