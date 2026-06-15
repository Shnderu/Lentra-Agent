from lentra.data.repositories.properties_repo import PropertiesRepository
from lentra.domain.scoring.ranking_engine import rank_properties
from lentra.domain.query.query_parser import parse_query


class SearchService:
    def __init__(self, db):
        self.repo = PropertiesRepository(db)

    def search(self, raw_query: str, budget_max: float | None = None):
        query_obj = parse_query(raw_query)

        properties = self.repo.search_properties(
            city=query_obj.city,
            budget_max=budget_max or query_obj.budget_max,
            pool=query_obj.pool,
            sea_view=query_obj.sea_view,
        )

        return rank_properties(properties, query_obj)
