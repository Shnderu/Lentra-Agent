# ============================================================
# MOCK SCRAPER SOURCE V15.9
# ============================================================

from typing import Dict, Any, List
import asyncio


class ScraperSource:
    name = "scraper"

    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.2)

        return [
            {
                "id": "scraper_1",
                "title": "Private Listing Studio",
                "city": query.get("city"),
                "price": 480,
                "rooms": 1,
                "source": self.name,
            }
        ]
