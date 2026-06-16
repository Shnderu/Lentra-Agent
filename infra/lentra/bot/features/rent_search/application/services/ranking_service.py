from typing import List
from lentra.bot.features.rent_search.models import RentalCard


class RentRankingService:
    """
    Simple deterministic ranking layer (MVP).

    Goal:
    - make results look "intelligent"
    - no ML yet, just heuristics
    """

    def rank(self, cards: List[RentalCard]) -> List[RentalCard]:
        def score(card: RentalCard):
            # higher score + lower price = better
            price_penalty = 0

            try:
                price_value = int("".join([c for c in card.price if c.isdigit()]))
                price_penalty = price_value / 1000
            except Exception:
                price_penalty = 0

            return card.score - price_penalty

        return sorted(cards, key=score, reverse=True)
