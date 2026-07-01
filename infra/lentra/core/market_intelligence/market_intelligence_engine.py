"""
CANONICAL STATE:

MarketIntelligenceEngine больше НЕ содержит собственной логики анализа.
Он является адаптером доменного API → AI OS gateway.
"""

from lentra.runtime.intelligence_gateway import interpret


class MarketIntelligenceEngine:

    def analyze(self, payload: dict) -> dict:
        """
        Единственный допустимый путь исполнения.
        """
        return interpret(payload)

    def evaluate(self, listing: dict, market: dict) -> dict:
        return interpret({
            "task": "evaluate_listing",
            "listing": listing,
            "market": market
        })

    def batch(self, listings: list, market: dict) -> dict:
        return interpret({
            "task": "evaluate_batch",
            "listings": listings,
            "market": market
        })
