from typing import List

from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.services.event_aggregator import EventAggregator


class LTRRanker:

    def __init__(self, dsn: str):

        self.aggregator = EventAggregator(dsn)
        self.cache = {}

    async def refresh(self):

        self.cache = await self.aggregator.compute_click_rates()

    def _key(self, item: RentSearchItem) -> str:
        return f"{item.city}:{item.title}"

    def rank(self, items: List[RentSearchItem]) -> List[RentSearchItem]:

        def score(item: RentSearchItem):

            key = self._key(item)

            ctr = self.cache.get(key, 0.0)

            base = getattr(item, "_score", 0.0)

            return base + ctr * 50

        return sorted(items, key=score, reverse=True)
