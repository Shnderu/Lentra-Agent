def fetch_vietnam_listings(query=None):
    """
    DATA LAYER v1 (STABLE MOCK MODE)

    NO SQL.
    NO FILTERING.
    RAW DATA ONLY.
    """

    data = [
        {
            "id": 1,
            "title": "Apartment near beach Nha Trang",
            "price": 500,
            "city": "Nha Trang",
            "source": "internal_seed",
            "geo": {"lat": 12.2388, "lng": 109.1967}
        },
        {
            "id": 2,
            "title": "Modern studio center HCMC",
            "price": 650,
            "city": "Ho Chi Minh",
            "source": "internal_seed",
            "geo": {"lat": 10.7769, "lng": 106.7009}
        },
        {
            "id": 3,
            "title": "Cheap room expat area",
            "price": 300,
            "city": "Da Nang",
            "source": "internal_seed",
            "geo": {"lat": 16.0544, "lng": 108.2022}
        }
    ]

    return data
