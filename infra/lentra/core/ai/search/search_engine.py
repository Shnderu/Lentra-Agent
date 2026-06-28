from lentra.core.market_intelligence.search.search_engine import SearchEngine


_engine = SearchEngine()


def search_listings(listings, query: dict):
    """
    Facade for pipeline compatibility
    """
    return _engine.search(listings, query or {})
