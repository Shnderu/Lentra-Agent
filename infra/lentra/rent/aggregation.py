# ============================================================
# LENTRA MULTI-SOURCE AGGREGATION V15.9
# ============================================================

from typing import Dict, Any, List
import hashlib
import asyncio


class AggregationEngine:
    def __init__(self, sources):
        self.sources = sources

    async def fetch_all(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        tasks = [s.fetch(query) for s in self.sources]
        results = await asyncio.gather(*tasks)

        merged = []
        for r in results:
            merged.extend(r)

        return merged


# ============================================================
# DEDUP ACROSS SOURCES
# ============================================================

def deduplicate_global(listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    unique = []

    for l in listings:
        key = hashlib.md5(
            f"{l.get('title')}_{l.get('price')}_{l.get('city')}".encode()
        ).hexdigest()

        if key in seen:
            continue

        seen.add(key)
        unique.append(l)

    return unique
