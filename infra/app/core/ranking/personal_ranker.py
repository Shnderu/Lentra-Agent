from typing import List
from lentra.core.contracts.listing_dto import ListingDTO


class PersonalRanker:

    def rank(self, listings: List[ListingDTO], session: dict):

        city_pref = session.get("city")
        budget_pref = session.get("budget")

        scored = []

        for l in listings:
            score = 0

            # 📍 city match boost
            if city_pref and l.city and l.city.lower() == city_pref.lower():
                score += 50

            # 💰 budget fit
            if budget_pref and l.price:
                if l.price <= budget_pref:
                    score += 30
                else:
                    score -= 20

            # 🧠 base quality boost (cheap listings slightly preferred)
            if l.price:
                score += max(0, 1000 - l.price) / 100

            scored.append((score, l))

        scored.sort(key=lambda x: x[0], reverse=True)

        return [l for score, l in scored]
