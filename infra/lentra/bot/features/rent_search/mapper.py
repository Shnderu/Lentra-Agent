from typing import List, Dict, Any
from lentra.bot.features.rent_search.contract.response import RentalCard


def map_to_cards(raw_items: List[Dict[str, Any]]) -> List[RentalCard]:
    cards: List[RentalCard] = []

    for item in raw_items:
        cards.append(
            RentalCard(
                title=item.get("title", "Object"),
                price=item.get("price", "—"),
                city=item.get("city", "—"),
                meta=item.get("meta", {}),
            )
        )

    return cards
