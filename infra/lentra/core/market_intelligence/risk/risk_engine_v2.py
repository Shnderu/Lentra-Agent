class RiskEngineV2:

    def process(self, listing: dict) -> dict:

        risk = listing.get("risk", 0.5)

        price = listing.get("price", 0)
        market_price = listing.get("market_price", price)

        deviation = abs(price - market_price) / max(market_price or 1, 1)

        listing["risk"] = min(1.0, risk + deviation * 0.3)

        listing["deviation"] = deviation * 100

        return listing
