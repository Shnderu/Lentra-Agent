from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)

from lentra.core.adapters.search_adapter import (
    SearchAdapter
)


class SearchHandler:
    """
    API search handler.

    Single flow:

    query
      |
      v
    SearchAdapter
      |
      v
    CanonicalSearchEntrypoint
      |
      v
    SearchPipeline
    """


    def __init__(self):

        self.adapter = SearchAdapter()

        self.pipeline = CanonicalSearchPipeline()

        self.entrypoint = CanonicalSearchEntrypoint(
            self.pipeline
        )



    def handle(
        self,
        query: str
    ):

        objects = self.adapter.build_objects(
            query
        )


        return self.entrypoint.execute(
            {
                "query": query,
                "objects": objects
            }
        )
