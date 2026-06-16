from typing import List
from lentra.bot.features.rent_search.models import RentalCard


def map_to_cards(raw_items: List[dict]) -> List[RentalCard]:
    cards = []

    for item in raw_items:
        cards.append(
            RentalCard(
                id=item["id"],
                title=item["title"],
                city=item["city"],
                price=f"{item['price']} {item.get('currency', '')}".strip(),
                score=float(item.get("score", 0)),
            )
        )

    return cards
