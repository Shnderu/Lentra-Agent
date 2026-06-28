from lentra.core.pipeline.canonical_search_pipeline import CanonicalSearchPipeline
from lentra.core.pipeline.canonical_entrypoint import CanonicalSearchEntrypoint


class SearchHandler:
    """
    API-level handler для search endpoint.

    ВАЖНО:
    - не содержит бизнес-логики
    - только передаёт objects в canonical pipeline
    """

    def __init__(self, dedup_engine=None, market_engine=None, ranking_engine=None):
        self.pipeline = CanonicalSearchPipeline(
            dedup_engine=dedup_engine,
            market_engine=market_engine,
            ranking_engine=ranking_engine,
        )

        self.entrypoint = CanonicalSearchEntrypoint(self.pipeline)

    def handle(self, objects):
        """
        Единственный допустимый путь обработки search результатов.
        """
        return self.entrypoint.execute(objects)
