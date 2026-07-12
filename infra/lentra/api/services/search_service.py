# ============================================================
# SEARCH SERVICE V19 - CANONICAL SEARCH ENTRY
# ============================================================

import time

from lentra.core.adapters.search_adapter import SearchAdapter
from lentra.core.pipeline.canonical_search_pipeline import (
    CanonicalSearchPipeline,
)
from lentra.core.pipeline.canonical_entrypoint import (
    CanonicalSearchEntrypoint,
)


class SearchService:
    """
    Unified search service.

    Architecture:

    API
      |
      v
    SearchService
      |
      v
    CanonicalSearchEntrypoint
      |
      v
    CanonicalSearchPipeline
      |
      v
    SearchPipeline
      |
      v
    Market Intelligence Core
    """

    def __init__(self):

        adapter = SearchAdapter()

        self.pipeline = CanonicalSearchPipeline()

        self.entrypoint = CanonicalSearchEntrypoint(
            self.pipeline
        )

        self.adapter = adapter


    async def search(self, request: dict):

        start = time.time()

        query = request.get(
            "query",
            ""
        )

        objects = self.adapter.build_objects(
            query
        )


        if not objects:

            return {
                "items": [],
                "count": 0,
                "query": query,
                "mode": "canonical_search_v19",
            }


        try:

            result = self.entrypoint.execute(
                {
                    "query": query,
                    "objects": objects,
                }
            )

        except Exception as e:

            return {
                "status": "error",
                "error": str(e),
                "query": query,
                "mode": "canonical_search_v19",
            }


        elapsed = round(
            time.time() - start,
            4
        )


        return {
            "items": result,
            "count": len(result)
            if isinstance(result, list)
            else 1,
            "query": query,
            "execution_time": elapsed,
            "mode": "canonical_search_v19",
        }
