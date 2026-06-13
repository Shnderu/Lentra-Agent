# ============================================================
# CONNECTOR AGGREGATION ENGINE V16.2
# ============================================================

from typing import List, Dict, Any
import asyncio


class ConnectorEngine:
    def __init__(self, connectors):
        self.connectors = connectors

    async def fetch_all(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        tasks = [c.fetch(query) for c in self.connectors]
        results = await asyncio.gather(*tasks)

        merged = []
        for r in results:
            merged.extend(r)

        return merged
