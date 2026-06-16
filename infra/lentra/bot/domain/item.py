from dataclasses import dataclass


@dataclass
class Item:
    id: str
    title: str
    city: str
    district: str
    price_vnd_mln: float
    score: float
