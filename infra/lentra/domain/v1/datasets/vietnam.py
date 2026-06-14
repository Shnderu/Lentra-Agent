def get_vietnam_properties(payload, state):
    """
    Static dataset (v1)
    Later will be replaced by DB or API
    """

    return [
        {
            "id": 1,
            "title": "Modern studio center",
            "price": 650,
            "city": "Ho Chi Minh",
            "tags": ["center", "modern"],
        },
        {
            "id": 2,
            "title": "Apartment near beach",
            "price": 500,
            "city": "Nha Trang",
            "tags": ["beach", "sea"],
        },
        {
            "id": 3,
            "title": "Cheap room expat area",
            "price": 300,
            "city": "Da Nang",
            "tags": ["cheap", "expat"],
        }
    ]
