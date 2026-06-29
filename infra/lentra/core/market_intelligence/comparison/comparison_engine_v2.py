class ComparisonEngineV2:

    def process(self, listing: dict) -> dict:

        price = listing.get("price", 0)
        market_price = listing.get("market_price", price)

        if market_price == 0:
            listing["price_vs_market"] = 0
        else:
            listing["price_vs_market"] = (price - market_price) / market_price * 100

        listing["attractiveness"] = max(0, 1 - abs(listing["price_vs_market"]) / 100)

        return listing
