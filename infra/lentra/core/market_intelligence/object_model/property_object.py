

class PropertyObject:

    def __init__(self, cluster_id: str, listings: list):

        self.cluster_id = cluster_id
        self.listings = listings

        self.prices = [l["price"] for l in listings]

        self.min_price = min(self.prices)
        self.max_price = max(self.prices)
        self.avg_price = sum(self.prices) / len(self.prices)

    def market_price(self):
        return self.avg_price

    def price_spread(self):
        return self.max_price - self.min_price

    def dominant_source(self):
        sources = {}
        for l in self.listings:
            src = l.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        return max(sources, key=sources.get)
