from lentra.core.market_intelligence.data.city_profiles import get_market_price


class QueryParser:

    CITY_ALIASES = {
        "da nang": "da_nang",
        "danang": "da_nang",
        "nha trang": "nha_trang",
        "nhatrang": "nha_trang",
        "bangkok": "bangkok",
        "bali": "bali",
        "chiang mai": "chiang_mai",
    }

    def __init__(self, query: str):
        self.query = query or ""

    def detect_city(self, text: str):
        for name, normalized in self.CITY_ALIASES.items():
            if name in text:
                return normalized

        return "da_nang"

    def extract_budget(self, text: str):
        import re

        match = re.search(r"(\d+)", text)

        if match:
            return int(match.group(1))

        return None

    def parse(self):
        text = self.query.lower()

        city = self.detect_city(text)

        return {
            "raw": self.query,
            "tokens": text.split(),
            "city": city,
            "budget": self.extract_budget(text),
            "market_price": get_market_price(city),
        }


def parse_query(query: str):
    return QueryParser(query).parse()
