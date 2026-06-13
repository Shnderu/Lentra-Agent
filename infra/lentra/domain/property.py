from dataclasses import dataclass


@dataclass
class Property:
    id: int
    title: str | None
    price_vnd_mln: float | None
    area_m2: float | None
    bedrooms: int | None
    bathrooms: int | None
    pet_friendly: bool | None
    pool: bool | None
    sea_view: bool | None
