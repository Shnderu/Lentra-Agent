from dataclasses import dataclass


@dataclass
class Card:
    id: str
    title: str
    city: str
    district: str
    price_vnd_mln: float
    score: float
    image: str | None = None
