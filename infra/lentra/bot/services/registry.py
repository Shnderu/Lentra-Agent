from dataclasses import dataclass
from typing import Any, Dict, List
import os

from lentra.bot.client import APIClient


@dataclass
class SearchResult:
    title: str
    price_vnd_mln: float
    city: str
    district: str
    score: float
    pool: bool = False
    sea_view: bool = False


class SearchService:
    def __init__(self):
        base_url = os.getenv("API_URL")

        if not base_url:
            raise RuntimeError("API_URL is not set")

        self.client = APIClient(base_url=base_url)

    async def search(self, query: str, budget_max: float = 10) -> List[SearchResult]:
        payload = {
            "query": query,
            "budget_max": budget_max
        }

        # ВАЖНО: путь без дублирования
        data: Dict[str, Any] = await self.client.post("/v1/search", payload)

        results = data.get("results", [])

        return [
            SearchResult(
                title=r.get("title"),
                price_vnd_mln=r.get("price_vnd_mln"),
                city=r.get("city"),
                district=r.get("district"),
                score=r.get("score"),
                pool=r.get("pool", False),
                sea_view=r.get("sea_view", False),
            )
            for r in results
        ]


search_service = SearchService()
