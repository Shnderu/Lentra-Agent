from lentra.core.adapters.fake_real_estate_api import FakeRealEstateAPI
from lentra.core.adapters.mock_rent_adapter import MockRentAdapter


# =========================
# REAL DATA ADAPTER LAYER v1
# =========================

class RentDataAdapterV1:
    """
    Единая точка получения данных по аренде.

    Приоритет:
    1) fake_real_estate_api (как primary source)
    2) mock_rent_adapter (fallback)
    """

    def __init__(self):
        self.primary = FakeRealEstateAPI()
        self.fallback = MockRentAdapter()

    async def get_rent_listings(self, query):
        try:
            data = await self.primary.fetch(query)

            if data:
                return self._normalize(data)

        except Exception:
            pass

        data = await self.fallback.fetch(query)
        return self._normalize(data)

    def _normalize(self, data):
        """
        Единый формат данных для core layer
        """

        normalized = []

        for item in data or []:
            normalized.append({
                "id": item.get("id"),
                "title": item.get("title"),
                "price": item.get("price"),
                "city": item.get("city"),
                "source": item.get("source", "unknown")
            })

        return normalized
