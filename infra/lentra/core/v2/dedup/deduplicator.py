from typing import List, Dict, Any
import hashlib


class DeduplicatorV2:
    """
    MVP entity clustering dedup engine

    Идея:
    - формируем стабильный fingerprint объекта
    - группируем одинаковые листинги
    """

    def _fingerprint(self, item: Dict[str, Any]) -> str:
        title = (item.get("title") or "").strip().lower()
        price = str(item.get("price") or "")
        location = (item.get("location") or "").strip().lower()

        raw = f"{title}|{price}|{location}"
        return hashlib.md5(raw.encode()).hexdigest()

    def deduplicate(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        groups = {}

        for item in listings:
            fp = self._fingerprint(item)

            if fp not in groups:
                item["duplicates"] = []
                item["cluster_id"] = fp
                groups[fp] = item
            else:
                groups[fp].setdefault("duplicates", []).append(item)

        return list(groups.values())


def deduplicate_v2(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    engine = DeduplicatorV2()
    return engine.deduplicate(listings)
