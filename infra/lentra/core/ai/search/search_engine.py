from lentra.core.market_intelligence.search.search_engine import (
    MarketSearchEngine,
)


_engine = MarketSearchEngine()


def search_listings(listings, query: dict):
    """
    Compatibility facade for AI search calls.
    Delegates to Market Intelligence search engine.
    """
    return _engine.search(
        listings,
        query or {},
    )
