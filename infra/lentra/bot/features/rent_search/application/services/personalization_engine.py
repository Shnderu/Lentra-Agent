from typing import List
from lentra.bot.features.rent_search.contracts import RentSearchItem


class PersonalizationEngine:

    def __init__(self, profile_repo):
        self.profile_repo = profile_repo

    async def rank(self, user_id: int, items: List[RentSearchItem]):

        profile = await self.profile_repo.get(user_id)

        def score(item: RentSearchItem):

            s = 0.0

            # city match boost
            if profile and profile.get("preferred_city"):
                if item.city == profile["preferred_city"]:
                    s += 40

            # price alignment
            if profile and profile.get("avg_price") and item.price_value:
                diff = abs(item.price_value - profile["avg_price"])
                s += max(0, 20 - diff / 1000)

            # base relevance
            s += getattr(item, "_score", 0.0)

            return s

        return sorted(items, key=score, reverse=True)
