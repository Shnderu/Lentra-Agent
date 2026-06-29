class MarketPriceEngine:

    def analyze(self, listing: dict) -> dict:

        price = listing.get("price", 0)

        if not price:
            return {
                "market_avg": 0,
                "currency": listing.get("currency", "USD")
            }

        # baseline approximation (temporary unified model)
        market_avg = price * 0.9

        return {
            "market_avg": market_avg,
            "currency": listing.get("currency", "USD")
        }
