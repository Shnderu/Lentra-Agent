# ============================================================
# MOCK LOCAL BOARD SOURCE V15.9
# ============================================================

from typing import Dict, Any, List
import asyncio


class LocalBoardSource:
    name = "local_board"

    async def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        await asyncio.sleep(0.2)

        return [
            {
                "id": "local_1",
                "title": "Cheap Apartment Near Center",
                "city": query.get("city"),
                "price": 420,
                "rooms": 2,
                "source": self.name,
            }
        ]
