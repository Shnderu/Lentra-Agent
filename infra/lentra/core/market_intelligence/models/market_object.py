
from dataclasses import dataclass, field
from typing import Any

from lentra.core.market_intelligence.models.listing import Listing


@dataclass(slots=True)
class MarketObject:

    id: str

    listings: list[Listing] = field(default_factory=list)

    market_price: float | None = None

    median_price: float | None = None

    price_deviation: float | None = None

    confidence: float = 0.0

    risk: float = 0.5

    area_score: float = 0.0

    area_profile: dict[str, Any] = field(default_factory=dict)

    negotiation: dict = field(default_factory=dict)

    verdict: str = "neutral"

    history: list = field(default_factory=list)

    def add_listing(self, listing: Listing):

        self.listings.append(listing)

    @property
    def sources(self):

        return sorted({l.source for l in self.listings})

    @property
    def listing_count(self):

        return len(self.listings)
