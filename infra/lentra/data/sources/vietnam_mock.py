from .base import BaseSource

class VietnamMockSource(BaseSource):
    def fetch(self):
        return [
            {
                "source": "mock_vn",
                "external_id": "vn_001",
                "title": "Studio District 1 Ho Chi Minh",
                "price": 450,
                "city": "HCMC",
                "district": "D1"
            },
            {
                "source": "mock_vn",
                "external_id": "vn_002",
                "title": "Modern Apartment District 2",
                "price": 380,
                "city": "HCMC",
                "district": "D2"
            }
        ]
