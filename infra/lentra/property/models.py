from pydantic import BaseModel


class Property(BaseModel):
    id: str
    source: str

    title: str
    url: str

    city: str
    district: str | None = None

    price: float
    currency: str = "USD"

    bedrooms: int | None = None
    bathrooms: int | None = None

    lat: float | None = None
    lng: float | None = None

    trust_score: float = 50

    photos: list[str] = []

    metadata: dict = {}
