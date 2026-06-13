# ============================================================
# MOCK CONNECTOR (MVP DATA SOURCE)
# ============================================================

class MockConnector:

    def fetch(self, query: str):
        return [
            {
                "id": 1,
                "title": "Modern apartment in Da Nang",
                "price": 450,
                "location_score": 80,
                "trust": 90
            },
            {
                "id": 2,
                "title": "Cheap studio near beach",
                "price": 300,
                "location_score": 60,
                "trust": 70
            },
            {
                "id": 3,
                "title": "Luxury condo city center",
                "price": 600,
                "location_score": 95,
                "trust": 85
            }
        ]
