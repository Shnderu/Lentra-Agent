from typing import List, Dict


class FlightRanker:

    def rank(self, items: List[Dict]) -> List[Dict]:

        def score(item):
            price = item.get("price", 999999)

            # простая эвристика (позже заменим ML)
            return price

        return sorted(items, key=score)
