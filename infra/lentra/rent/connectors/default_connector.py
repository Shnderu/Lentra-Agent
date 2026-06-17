from typing import Dict, Any, List

from lentra.rent.providers import MockRentProvider


class DefaultConnector:
    """
    Основной connector для rent_search.
    Теперь поддерживает fallback provider без внешних API.
    """

    def __init__(self):
        self.provider = MockRentProvider()

    def search(self, query: Dict[str, Any]) -> Dict[str, Any]:
        items = self.provider.search(query)

        return {
            "source": "default_connector",
            "query": query,
            "items": items
        }
