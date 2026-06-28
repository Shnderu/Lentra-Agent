
from lentra.core.market_intelligence.models.market_object import MarketObject
from lentra.core.market_intelligence.models.listing import Listing


class DuplicateEngine:

    def run(self, objects: list[MarketObject]) -> list[MarketObject]:

        clusters = []

        used = set()

        for i, obj in enumerate(objects):

            if i in used:
                continue

            cluster = MarketObject(
                id=obj.id
            )

            self._merge(cluster, obj)

            for j, other in enumerate(objects):

                if i == j or j in used:
                    continue

                if self._is_duplicate(obj, other):

                    self._merge(cluster, other)
                    used.add(j)

            clusters.append(cluster)

        return clusters

    def _merge(self, target: MarketObject, source: MarketObject):

        for l in source.listings:

            if not any(x.id == l.id for x in target.listings):

                target.add_listing(l)

        # merge numeric signals safely

        target.market_price = self._avg(
            target.market_price,
            source.market_price
        )

        target.risk = max(
            target.risk,
            source.risk
        )

        target.area_score = max(
            target.area_score,
            source.area_score
        )

    def _is_duplicate(self, a: MarketObject, b: MarketObject) -> bool:

        # rule 1: shared source OR shared text signal
        a_sources = set(a.sources)
        b_sources = set(b.sources)

        if a_sources & b_sources:

            return True

        # rule 2: price proximity
        if a.market_price and b.market_price:

            if abs(a.market_price - b.market_price) < 80:

                return True

        # rule 3: title similarity (very rough v1)
        a_titles = {l.title.lower() for l in a.listings}
        b_titles = {l.title.lower() for l in b.listings}

        if a_titles & b_titles:

            return True

        return False

    def _avg(self, a, b):

        values = [v for v in [a, b] if v is not None]

        if not values:
            return None

        return sum(values) / len(values)
