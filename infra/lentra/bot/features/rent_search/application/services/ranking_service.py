from typing import List

from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.application.services.text_normalizer import TextNormalizer


class RankingService:

    SOURCE_WEIGHT = {
        "scraper": 30,
        "mock_th": 10,
        "social": 5,
        None: 1
    }

    MIN_SCORE_THRESHOLD = 60  # 👈 КЛЮЧЕВОЙ ПОРЯДОК КАЧЕСТВА

    def _tokenize(self, text: str) -> set:
        return set((text or "").lower().split())

    def rank(
        self,
        items: List[RentSearchItem],
        context: SearchContext
    ) -> List[RentSearchItem]:

        query_tokens = self._tokenize(context.query)

        def score(item: RentSearchItem):

            s = 0.0

            # city match
            item_city = TextNormalizer.normalize_city(getattr(item, "city", None))
            context_city = TextNormalizer.normalize_city(context.city)

            if context_city and item_city == context_city:
                s += 50

            # price scoring
            if item.price_value is not None:

                if context.min_price is not None and item.price_value >= context.min_price:
                    s += 10

                if context.max_price is not None and item.price_value <= context.max_price:
                    s += 10

            # source weight
            source = getattr(item, "source", None)
            s += self.SOURCE_WEIGHT.get(source, 1)

            # query relevance
            title_tokens = self._tokenize(getattr(item, "title", ""))

            if query_tokens:
                overlap = len(query_tokens & title_tokens)
                s += overlap * 15

            # base bias
            s += 1

            return s

        scored = [(item, score(item)) for item in items]

        # -------------------------
        # QUALITY FILTER (NEW)
        # -------------------------
        filtered = [
            item for item, s in scored
            if s >= self.MIN_SCORE_THRESHOLD
        ]

        return sorted(filtered, key=lambda x: score(x), reverse=True)
