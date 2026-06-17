from typing import List
from app.core.contracts.response_dto import RentResponseDTO
from app.core.ranking.advanced_ranker import AdvancedRanker


class RentAggregator:

    def __init__(self):
        self.ranker = AdvancedRanker()

    def aggregate(self, query: str, sources: List[List], session=None):

        flat = []
        for source in sources:
            flat.extend(source)

        # dedup
        seen = set()
        unique = []

        for item in flat:
            key = (item.title, item.price, item.city)
            if key in seen:
                continue
            seen.add(key)
            unique.append(item)

        # 🔥 ADVANCED RANKING
        if session:
            unique = self.ranker.rank(unique, session)

        else:
            unique.sort(key=lambda x: x.price or 10**9)

        return RentResponseDTO(
            query=query,
            listings=unique,
            total=len(unique)
        )
