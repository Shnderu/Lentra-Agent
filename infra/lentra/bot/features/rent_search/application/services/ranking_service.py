from typing import List
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class RankingService:
    """
    Простая scoring-модель (пока rule-based)
    """

    def rank(
        self,
        items: List[RentSearchItem],
        context: SearchContext
    ) -> List[RentSearchItem]:

        def score(item: RentSearchItem) -> float:
            s = 0.0

            # город совпадает
            if context.city and item.city.lower() == context.city:
                s += 50

            # цена (очень грубо)
            try:
                price_val = int(''.join(filter(str.isdigit, item.price)))
                if context.min_price and price_val >= context.min_price:
                    s += 10
                if context.max_price and price_val <= context.max_price:
                    s += 10
            except:
                pass

            # базовый вес
            s += 1
            return s

        return sorted(items, key=score, reverse=True)
