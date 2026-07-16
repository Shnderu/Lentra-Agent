from lentra.db.repositories.property_repo import PropertyRepository


class PropertyService:
    """
    Application service for canonical PropertyDB flow.

    Responsibilities:
    - coordinate repository access
    - transform ORM objects to output DTO-like dicts

    Not responsible for:
    - ranking
    - scoring
    - market intelligence
    """


    def __init__(
        self,
        repo: PropertyRepository
    ):
        self.repo = repo


    def search(
        self,
        query: str = "",
        budget_max: float | None = None,
        city: str | None = None,
    ):

        properties = self.repo.search(
            city=city,
            budget_max=budget_max
        )


        results = []

        for prop in properties:

            results.append(
                {
                    "id": prop.id,
                    "title": prop.title,
                    "price_vnd_mln": prop.price_vnd_mln,
                    "area_m2": prop.area_m2,
                    "city": prop.city,
                    "district": prop.district,
                    "pool": prop.pool,
                    "sea_view": prop.sea_view,
                    "score": prop.score,
                }
            )


        return results
