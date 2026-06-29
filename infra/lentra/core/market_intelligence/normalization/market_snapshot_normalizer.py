class MarketSnapshotNormalizer:

    def normalize(self, listings: list) -> dict:

        if not listings:
            return {
                "market_avg_price": 0,
                "price_std": 0,
                "count": 0
            }

        prices = [float(l.get("price", 0) or 0) for l in listings if l.get("price") is not None]

        if not prices:
            return {
                "market_avg_price": 0,
                "price_std": 0,
                "count": len(listings)
            }

        avg = sum(prices) / len(prices)

        variance = sum((p - avg) ** 2 for p in prices) / len(prices)
        std = variance ** 0.5

        return {
            "market_avg_price": round(avg, 2),
            "price_std": round(std, 2),
            "count": len(listings)
        }


    def enrich_listing(self, listing: dict, snapshot: dict) -> dict:

        price = float(listing.get("price") or 0)
        market_avg = snapshot.get("market_avg_price") or price

        if market_avg == 0:
            market_avg = price

        deviation = (price - market_avg) / market_avg if market_avg else 0

        listing["market_avg"] = market_avg
        listing["price_deviation"] = round(deviation, 4)

        return listing
