from typing import Dict, Any


class GeoRouterV2:
    """
    MVP geo router v2:
    - определяет страну и город из текста
    - без ML, только правила (MVP stage)
    """

    COUNTRY_MAP = {
        "da nang": ("vietnam", "da nang"),
        "hanoi": ("vietnam", "hanoi"),
        "ho chi minh": ("vietnam", "ho chi minh"),

        "bali": ("indonesia", "bali"),
        "canggu": ("indonesia", "bali"),
        "ubud": ("indonesia", "bali"),

        "bangkok": ("thailand", "bangkok"),
        "chiang mai": ("thailand", "chiang mai"),
        "phuket": ("thailand", "phuket"),
    }

    DEFAULT = ("vietnam", "da nang")

    def route(self, query: Dict[str, Any]) -> Dict[str, Any]:

        raw = (query.get("raw") or "").lower()

        for key, (country, city) in self.COUNTRY_MAP.items():
            if key in raw:
                return {
                    **query,
                    "country": country,
                    "city": city
                }

        return {
            **query,
            "country": self.DEFAULT[0],
            "city": self.DEFAULT[1]
        }
