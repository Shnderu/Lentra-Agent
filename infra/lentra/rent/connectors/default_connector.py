from typing import Dict, Any, List

from lentra.rent.providers import MockRentProvider


class DefaultConnector:
    """
    Connector слой для rent_search.
    Контракт строго: fetch(query) -> dict
    """

    def __init__(self):
        self.provider = MockRentProvider()

    def fetch(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """
        ЕДИНЫЙ контракт для service layer
        """
        items: List[Dict[str, Any]] = self.provider.search(query)

        return {
            "source": "default_connector",
            "query": query,
            "items": items
        }
