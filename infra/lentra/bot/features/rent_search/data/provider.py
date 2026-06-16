from typing import List, Dict, Any


class RentDataProvider:
    """
    Абстракция источника данных.
    В будущем: Avito / Cian / custom API / scraping layer
    """

    def fetch(self, query: str) -> List[Dict[str, Any]]:
        raise NotImplementedError
