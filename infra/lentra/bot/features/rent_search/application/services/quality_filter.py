from typing import List

from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class RentQualityFilter:

    def __init__(self):
        pass

    def filter(self, items: List[RentSearchItem]) -> List[RentSearchItem]:

        result = []

        for item in items:

            # 1. базовая валидация
            if not item.title or not item.city:
                continue

            # 2. price_value sanity check
            if item.price_value is not None:

                # отсекать отрицательные и нули
                if item.price_value <= 0:
                    continue

                # отсекать явно мусорные значения
                if item.price_value > 1_000_000:
                    continue

            # 3. title sanity (минимальная длина)
            if len(item.title.strip()) < 5:
                continue

            result.append(item)

        return result
