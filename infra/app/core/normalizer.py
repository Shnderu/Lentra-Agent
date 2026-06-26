from typing import Dict, Any, List
from lentra.core.models import ListingDTO


class ListingNormalizer:
    """
    Приводит любые источники к единому контракту ListingDTO
    """

    def normalize(self, data: Dict[str, Any], source: str) -> ListingDTO:
        return ListingDTO(
            title=self._title(data),
            price=self._price(data),
            city=self._city(data),
            room_type=self._room_type(data),
            source=source,
            raw_score=data.get("score", None)
        )

    def normalize_batch(self, items: List[Dict[str, Any]], source: str) -> List[ListingDTO]:
        return [self.normalize(i, source) for i in items]

    def _title(self, d): return d.get("title") or d.get("name") or "unknown"

    def _price(self, d):
        try:
            return int(d.get("price") or 0)
        except:
            return 0

    def _city(self, d): return d.get("city") or d.get("location")

    def _room_type(self, d): return d.get("type") or d.get("room_type")
