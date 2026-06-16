from typing import List, Dict, Any
from lentra.bot.features.rent_search.contracts import RentSearchItem


def map_to_cards(raw: List[Dict[str, Any]]) -> List[RentSearchItem]:
    """
    Чистый трансформер:
    dict → domain model
    """

    result: List[RentSearchItem] = []

    for item in raw:
        result.append(
            RentSearchItem(
                title=item.get("title", ""),
                price=item.get("price", ""),
                city=item.get("city", ""),
                meta=item.get("meta", {})
            )
        )

    return result
