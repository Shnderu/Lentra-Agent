class NegotiationEngineV1:

    def score(self, listing):

        price = listing.get("price", 0)
        market = listing.get("market_price", price)

        # bargaining power estimate
        advantage = (market - price) / max(market, 1)

        listing["negotiation"] = {
            "bargaining_power": round(advantage, 3),
            "can_negotiate": advantage > 0.1,
            "strategy": "aggressive" if advantage > 0.2 else "moderate" if advantage > 0.05 else "weak"
        }

        return listing
