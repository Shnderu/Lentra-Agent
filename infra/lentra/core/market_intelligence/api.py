from lentra.runtime.intelligence_enforcer import run_intelligence


class MarketIntelligence:
    """
    CANONICAL WRAPPER

    Больше НЕ содержит логики.
    Только проксирует в AI OS через gateway.
    """

    def evaluate_listing(self, listing: dict, market: dict) -> dict:
        return run_intelligence({
            "task": "evaluate_listing",
            "listing": listing,
            "market": market
        })

    def evaluate_batch(self, listings: list, market: dict) -> dict:
        return run_intelligence({
            "task": "evaluate_batch",
            "listings": listings,
            "market": market
        })
