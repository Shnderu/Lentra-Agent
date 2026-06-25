from typing import List
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class SemanticScorer:

    """
    v1 stub semantic scorer.
    Сейчас без ML — rule-based fallback,
    позже заменим на embeddings (OpenAI / local model).
    """

    KEYWORDS = {
        "apartment": ["apartment", "condo", "flat", "studio"],
        "luxury": ["luxury", "premium", "high-end"],
        "cheap": ["cheap", "budget", "affordable"],
        "beach": ["beach", "sea", "ocean"],
        "center": ["center", "downtown", "central"]
    }

    def score(self, text: str, query: str) -> float:

        if not text or not query:
            return 0.0

        text = text.lower()
        query = query.lower()

        score = 0.0

        # прямое вхождение
        if any(word in text for word in query.split()):
            score += 5

        # keyword overlap
        for k, variants in self.KEYWORDS.items():

            if k in query:
                if any(v in text for v in variants):
                    score += 3

        return score


    def boost(
        self,
        items: List[RentSearchItem],
        context: SearchContext
    ) -> List[RentSearchItem]:

        query = context.query

        def compute(item: RentSearchItem):

            base = getattr(item, "_score", 0.0)

            semantic = self.score(
                text=item.title,
                query=query
            )

            return base + semantic

        return sorted(
            items,
            key=compute,
            reverse=True
        )
