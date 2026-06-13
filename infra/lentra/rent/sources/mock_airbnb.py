# ============================================================
# MOCK AIRBNB SOURCE V15.9
# ============================================================

from typing import Dict, Any, List
import asyncio


class AirbnbSource:
    name = "airbnb"

    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.2)

        return [
            {
                "id": "airbnb_1",
                "title": "Airbnb Modern Studio",
                "city": query.get("city"),
                "price": 500,
                "rooms": 1,
                "source": self.name,
            }
        ]
