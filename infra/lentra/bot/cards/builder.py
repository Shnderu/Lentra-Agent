from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Card:
    id: str
    title: str
    location: str
    price: str
    score: float
    features: list
    raw: Dict[str, Any]


class CardBuilder:

    def build(self, item: dict) -> Card:
        features = []

        if item.get("pool"):
            features.append("🏊 бассейн")
        if item.get("sea_view"):
            features.append("🌊 вид на море")

        location = f"{item.get('city', '')} · {item.get('district', '')}"

        price = f"{item.get('price_vnd_mln', 0)} млн VND"

        return Card(
            id=str(item.get("id")),
            title=item.get("title", ""),
            location=location,
            price=price,
            score=float(item.get("score", 0)),
            features=features,
            raw=item
        )
