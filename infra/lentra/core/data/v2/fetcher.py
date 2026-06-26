from typing import Dict, Any, List


class GeoFetcherV2:
    """
    MVP geo-aware fetcher:
    - маршрутизация источников по стране
    - пока mock-данные, но структура готова под реальные коннекторы
    """

    def fetch(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:

        country = query.get("country", "vietnam")
        city = query.get("city", "da nang")

        if country == "vietnam":
            return self._vietnam(city)

        if country == "thailand":
            return self._thailand(city)

        if country == "indonesia":
            return self._indonesia(city)

        return self._vietnam(city)

    def _vietnam(self, city: str):
        return [
            {
                "id": "vn-1",
                "title": "Studio near beach",
                "price": 700,
                "currency": "USD",
                "location": city,
                "source": "facebook_vn"
            },
            {
                "id": "vn-2",
                "title": "Modern apartment center",
                "price": 650,
                "currency": "USD",
                "location": city,
                "source": "telegram_vn"
            }
        ]

    def _thailand(self, city: str):
        return [
            {
                "id": "th-1",
                "title": "Condo Bangkok center",
                "price": 900,
                "currency": "USD",
                "location": city,
                "source": "facebook_th"
            }
        ]

    def _indonesia(self, city: str):
        return [
            {
                "id": "id-1",
                "title": "Villa near beach Bali",
                "price": 1200,
                "currency": "USD",
                "location": city,
                "source": "facebook_id"
            }
        ]
