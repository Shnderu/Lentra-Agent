from typing import Dict, Any

from lentra.rent.connectors.default_connector import DefaultConnector
from lentra.rent.quality.pipeline import RentQualityPipeline


class RentSearchService:

    def __init__(self, repository=None):
        # repository пока не используем (убираем ложную зависимость)
        self.connector = DefaultConnector()
        self.quality = RentQualityPipeline()

    async def search(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        query = {
            "text": payload.get("text"),
            "user_id": payload.get("user_id")
        }

        raw = self.connector.fetch(query)

        items = raw.get("items", [])

        processed = self.quality.process(items)

        return {
            "text": "rent_search v4",
            "raw": [raw],
            "items": processed
        }
