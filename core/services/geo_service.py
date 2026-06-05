class GeoService:
    def to_iata(self, text: str) -> str | None:
        text = text.lower()

        mapping = {
            "москва": "MOW",
            "питер": "LED",
            "санкт-петербург": "LED",
            "стамбул": "IST",
            "дубай": "DXB",
            "алматы": "ALA"
        }

        for city, code in mapping.items():
            if city in text:
                return code

        return None


geo_service = GeoService()
