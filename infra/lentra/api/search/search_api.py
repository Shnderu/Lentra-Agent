

from lentra.core.ai.semantic_search.embeddings.embedding_engine import embed
from lentra.core.ai.semantic_search.vector_store.vector_store import search
from lentra.core.pipeline.pipeline import LentraPipeline
from lentra.core.ai.concierge.ranker.ranking_engine import rank_listings


class SearchAPI:

    def __init__(self):
        self.pipeline = LentraPipeline()

    def search_candidates(self, query: str):

        raw_candidates = search(embed(query))

        results = []

        for c in raw_candidates:

            enriched = self.pipeline.run({
                "id": c.get("id"),
                "title": c.get("title"),
                "price": c.get("price"),
                "currency": "USD",
                "city": "",
                "location": "",
                "source": "vector"
            })

            results.append({
                "listing": enriched,
                "reason": "vector_match"
            })

        ranked = rank_listings(results)

        return ranked
