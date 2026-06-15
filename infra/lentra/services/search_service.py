from typing import List, Optional
from lentra.repositories.apartment_repository import ApartmentRepository
from lentra.services.scoring import calculate_score


class SearchService:

    def __init__(self, db):
        self.repo = ApartmentRepository(db)

    def search(self, query: str, budget_max: Optional[float] = None):

        # 1. пока упрощённый парсинг (без NLP)
        city = self._extract_city(query)

        # 2. получить кандидатов из БД
        candidates = self.repo.search_candidates(city=city)

        results = []

        for apt in candidates:
            score = calculate_score(
                apt,
                budget_max=budget_max,
                query=query
            )

            results.append({
                "id": apt["id"],
                "title": apt["title"],
                "price_vnd_mln": apt["price_vnd_mln"],
                "area_m2": apt["area_m2"],
                "city": apt["city"],
                "district": apt["district"],
                "pool": apt["pool"],
                "sea_view": apt["sea_view"],
                "score": score
            })

        # 3. сортировка
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query": query,
            "results": results
        }

    def _extract_city(self, query: str) -> Optional[str]:
        q = query.lower()

        if "da nang" in q:
            return "Da Nang"
        if "hanoi" in q:
            return "Hanoi"
        if "saigon" in q or "ho chi minh" in q:
            return "Ho Chi Minh"

        return None
