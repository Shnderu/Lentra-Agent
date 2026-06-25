from typing import List

from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class RankingService:

    CITY_ALIASES = {
        "da nang": "da_nang",
        "danang": "da_nang",
        "nha trang": "nha_trang",
        "ho chi minh": "ho_chi_minh",
        "saigon": "ho_chi_minh",
        "hanoi": "hanoi",
        "bangkok": "bangkok",
        "phuket": "phuket",
        "chiang mai": "chiang_mai",
    }

    def rank(
        self,
        items: List[RentSearchItem],
        context: SearchContext
    ) -> List[RentSearchItem]:

        def normalize_city(city: str | None):
            if not city:
                return None

            return self.CITY_ALIASES.get(
                city.lower().strip(),
                city.lower().strip()
            )

        def score(item: RentSearchItem):

            s = 0.0

            item_city = normalize_city(getattr(item, "city", None))

            if context.city and item_city == context.city:
                s += 50

            # ✅ теперь используем нормализованную цену
            if item.price_value is not None:

                if context.min_price is not None:
                    if item.price_value >= context.min_price:
                        s += 10

                if context.max_price is not None:
                    if item.price_value <= context.max_price:
                        s += 10

            # базовый вес
            s += 1

            return s

        return sorted(items, key=score, reverse=True)
