from lentra.runtime.intelligence_gateway import interpret


class MarketIntelligence:
    """
    DEPRECATED LOGIC WRAPPER
    Всё решение принимает внешний AI engine
    """

    def evaluate_listing(self, listing: dict, market: dict) -> dict:
        return interpret({
            "listing": listing,
            "market": market,
            "task": "evaluate_listing"
        })

    def evaluate_batch(self, listings: list, market: dict) -> dict:
        return interpret({
            "listings": listings,
            "market": market,
            "task": "evaluate_batch"
        })
