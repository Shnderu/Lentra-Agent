from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import search

from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline
)

from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint
)

from lentra.core.adapters.search_adapter import SearchAdapter


class SearchAPI:
    """
    Vector search API.

    Flow:

    query
      |
      v
    vector candidates
      |
      v
    canonical entrypoint
      |
      v
    SearchPipeline
      |
      v
    Market Intelligence
    """

    def __init__(self):

        self.adapter = SearchAdapter()

        self.pipeline = CanonicalSearchPipeline()

        self.entrypoint = CanonicalSearchEntrypoint(
            self.pipeline
        )

    def search_candidates(
        self,
        query: str
    ):

        raw_candidates = search(
            embed(query)
        )

        if not raw_candidates:
            return []

        objects = []

        for item in raw_candidates:

            objects.append(
                {
                    "id": item.get("id"),
                    "title": item.get("title", ""),
                    "price": item.get("price", 0),
                    "currency": "USD",
                    "city": item.get("city", "Da Nang"),
                    "location": item.get("location", ""),
                    "source": "vector",
                    "query": query,
                }
            )

        return self.entrypoint.execute(
            {
                "query": query,
                "objects": objects,
            }
        )
