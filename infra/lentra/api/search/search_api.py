

from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import search


class SearchAPI:

    def search_candidates(self, query: str):

        # ALWAYS USE VECTOR SEARCH (NO FALLBACKS)

        vector = embed(query)

        results = search(vector)

        if not results:
            return []

        return results
