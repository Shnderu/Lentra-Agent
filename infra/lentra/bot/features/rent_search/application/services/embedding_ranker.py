from typing import List
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.application.services.embedding_service import EmbeddingService


class EmbeddingRanker:

    def __init__(self):
        self.embedder = EmbeddingService()

    def _build_query_text(self, context: SearchContext) -> str:

        parts = [
            context.query or "",
            context.city or "",
            context.country or ""
        ]

        return " ".join([p for p in parts if p])


    def _build_item_text(self, item: RentSearchItem) -> str:

        parts = [
            item.title or "",
            item.city or "",
            item.country or ""
        ]

        return " ".join([p for p in parts if p])


    def boost(
        self,
        items: List[RentSearchItem],
        context: SearchContext
    ) -> List[RentSearchItem]:

        try:
            query_text = self._build_query_text(context)
            query_vec = self.embedder.embed(query_text)

            def score(item: RentSearchItem):

                item_text = self._build_item_text(item)
                item_vec = self.embedder.embed(item_text)

                base = getattr(item, "_score", 0.0)

                similarity = self.embedder.similarity(query_vec, item_vec)

                # усиление за качество сигнала
                return base + (similarity * 25.0)

            return sorted(items, key=score, reverse=True)

        except Exception:
            return items
