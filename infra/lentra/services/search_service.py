from lentra.repositories.apartment_repo import ApartmentRepository

class SearchService:

    def __init__(self, db):
        self.repo = ApartmentRepository(db)

    def search(self, query: str, budget_max: float):
        city = "Da Nang" if "da nang" in query.lower() else None

        results = self.repo.search(
            city=city,
            max_price=budget_max
        )

        return {
            "query": query,
            "results": [
                {
                    "id": r.id,
                    "title": r.title,
                    "price_vnd_mln": r.price_vnd_mln,
                    "area_m2": r.area_m2,
                    "city": r.city,
                    "district": r.district,
                    "pool": r.pool,
                    "sea_view": r.sea_view,
                }
                for r in results
            ]
        }
