from lentra.core.pipeline.canonical_search_pipeline import CanonicalSearchPipeline
from lentra.core.pipeline.canonical_entrypoint import CanonicalSearchEntrypoint
from lentra.core.adapters.search_adapter import SearchAdapter


class SearchHandler:
    """
    API handler:
    GET /search?q=...
    """

    def __init__(self, dedup_engine=None, market_engine=None, ranking_engine=None):
        self.adapter = SearchAdapter()

        self.pipeline = CanonicalSearchPipeline(
            dedup_engine=dedup_engine,
            market_engine=market_engine,
            ranking_engine=ranking_engine,
        )

        self.entrypoint = CanonicalSearchEntrypoint(self.pipeline)

    def handle(self, query: str):
        """
        Полный flow:
        query → objects → pipeline → response
        """

        objects = self.adapter.build_objects(query)
        return self.entrypoint.execute(objects)
