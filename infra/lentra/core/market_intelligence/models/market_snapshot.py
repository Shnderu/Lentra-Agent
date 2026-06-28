
from dataclasses import dataclass, field
from lentra.core.market_intelligence.models.market_object import MarketObject


@dataclass(slots=True)
class MarketSnapshot:

    query: str

    objects: list[MarketObject] = field(default_factory=list)

    total_objects: int = 0

    average_market_price: float | None = None

    def finalize(self):

        self.total_objects = len(self.objects)

        prices = [
            o.market_price
            for o in self.objects
            if o.market_price is not None
        ]

        if prices:

            self.average_market_price = sum(prices) / len(prices)

        return self
