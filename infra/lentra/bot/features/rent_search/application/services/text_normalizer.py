class TextNormalizer:

    CITY_ALIASES = {
        "da nang": "da_nang",
        "danang": "da_nang",
        "ho chi minh": "ho_chi_minh",
        "saigon": "ho_chi_minh",
        "hanoi": "hanoi",
        "bangkok": "bangkok",
        "phuket": "phuket",
        "chiang mai": "chiang_mai",
        "nha trang": "nha_trang",
    }

    @classmethod
    def normalize_city(cls, city: str | None) -> str | None:
        if not city:
            return None

        city = city.lower().strip()
        return cls.CITY_ALIASES.get(city, city)
