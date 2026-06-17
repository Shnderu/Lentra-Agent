from typing import List, Dict, Any


class MockRentProvider:
    """
    Детеминированный источник данных для rent_search v3/v4.
    Используется как fallback, пока нет внешних API.
    """

    def search(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = (query.get("text") or "").lower()

        # минимальный набор тестовых объектов
        dataset = [
            {
                "id": "apt_1",
                "title": "1BR Apartment near BTS",
                "price": 450,
                "city": "Bangkok",
                "source": "mock"
            },
            {
                "id": "apt_2",
                "title": "Studio in center",
                "price": 300,
                "city": "Bangkok",
                "source": "mock"
            },
            {
                "id": "apt_3",
                "title": "Sea view condo",
                "price": 800,
                "city": "Phuket",
                "source": "mock"
            }
        ]

        # простейший фильтр
        if not text:
            return dataset

        return [
            item for item in dataset
            if text in item["title"].lower()
            or text in item["city"].lower()
        ]
