from lentra.db.repositories.apartment_repository import ApartmentRepository


class SearchService:
    def __init__(self, repo: ApartmentRepository):
        self.repo = repo

    def search(self, query: str, budget_max: float | None = None):
        # 1. простая нормализация запроса
        query_lower = query.lower()

        city = None
        if "da nang" in query_lower:
            city = "Da Nang"

        # 2. получаем кандидатов из БД
        apartments = self.repo.search_basic(
            city=city,
            max_price=budget_max
        )

        # 3. scoring engine (v1)
        results = []
        for a in apartments:
            score = 0.0

            if a.pool:
                score += 0.5
            if a.sea_view:
                score += 0.3
            if a.price_vnd_mln <= (budget_max or 999):
                score += 0.2

            results.append({
                "id": a.id,
                "title": a.title,
                "price_vnd_mln": a.price_vnd_mln,
                "area_m2": a.area_m2,
                "city": a.city,
                "district": a.district,
                "pool": a.pool,
                "sea_view": a.sea_view,
                "score": round(score, 3)
            })

        # 4. сортировка
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "query": query,
            "results": results
        }
