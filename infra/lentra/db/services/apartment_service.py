from lentra.db.repositories.apartment_repo import ApartmentRepository


class ApartmentService:

    def __init__(self, repo: ApartmentRepository):
        self.repo = repo

    def search(self, query: str, budget_max: float):
        raw = self.repo.search(budget_max=budget_max)

        results = []
        for a in raw:
            score = self._score(a, query)

            results.append({
                "id": a.id,
                "title": a.title,
                "price_vnd_mln": a.price_vnd_mln,
                "area_m2": a.area_m2,
                "city": a.city,
                "district": a.district,
                "pool": a.pool,
                "sea_view": a.sea_view,
                "score": score
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)

    def _score(self, a, query: str) -> float:
        score = 0.0

        if a.pool:
            score += 0.4
        if a.sea_view:
            score += 0.3
        if a.price_vnd_mln <= 10:
            score += 0.3

        return score
