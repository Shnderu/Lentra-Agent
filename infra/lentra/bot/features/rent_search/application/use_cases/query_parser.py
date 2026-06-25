import re

from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class QueryParser:

    CITY_MAP = {
        "nha trang": ("nha_trang", "vietnam"),
        "nhatrang": ("nha_trang", "vietnam"),
        "дананг": ("da_nang", "vietnam"),
        "da nang": ("da_nang", "vietnam"),
        "danang": ("da_nang", "vietnam"),
        "сайгон": ("ho_chi_minh", "vietnam"),
        "ho chi minh": ("ho_chi_minh", "vietnam"),
        "hcmc": ("ho_chi_minh", "vietnam"),
        "ханой": ("hanoi", "vietnam"),
        "hanoi": ("hanoi", "vietnam"),

        "bangkok": ("bangkok", "thailand"),
        "phuket": ("phuket", "thailand"),
        "chiang mai": ("chiang_mai", "thailand"),
    }

    def parse(self, raw_query: str) -> SearchContext:

        query = raw_query.lower().strip()

        city, country = self._extract_location(query)

        min_price, max_price = self._extract_price(query)

        cleaned_query = self._clean(query)

        return SearchContext(
            raw_query=raw_query,
            query=cleaned_query,
            city=city,
            country=country,
            min_price=min_price,
            max_price=max_price,
        )

    def _extract_location(self, text: str):

        for key, value in self.CITY_MAP.items():
            if key in text:
                return value

        return None, None

    def _extract_price(self, text: str):

        match = re.search(r"(\d+)\s*-\s*(\d+)", text)

        if match:
            return (
                int(match.group(1)),
                int(match.group(2))
            )

        return None, None

    def _clean(self, text: str):

        text = re.sub(
            r"\d+\s*-\s*\d+",
            "",
            text
        )

        return text.strip()
