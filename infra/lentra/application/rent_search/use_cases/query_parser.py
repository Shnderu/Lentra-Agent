import re
from lentra.application.rent_search.dto.search_context import SearchContext


class QueryParser:
    """
    Преобразует сырой текст в структурированный SearchContext
    """

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

    COUNTRY_ALIASES = {
        "vietnam": "vietnam",
        "thailand": "thailand",
        "vn": "vietnam",
        "th": "thailand",
    }

    def parse(self, raw_query: str) -> SearchContext:
        query = raw_query.lower().strip()

        city = self._extract_city(query)
        country = self._extract_country(query)

        min_price, max_price = self._extract_price(query)

        cleaned_query = self._clean(query)

        return SearchContext(
            raw_query=raw_query,
            query=cleaned_query,
            city=city,
            country=country,
            min_price=min_price,
            max_price=max_price
        )

    def _extract_city(self, text: str):
        for k, v in self.CITY_ALIASES.items():
            if k in text:
                return v
        return None

    def _extract_country(self, text: str):
        for k, v in self.COUNTRY_ALIASES.items():
            if k in text:
                return v
        return None

    def _extract_price(self, text: str):
        match = re.search(r"(\d+)\s*-\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def _clean(self, text: str) -> str:
        text = re.sub(r"\d+\s*-\s*\d+", "", text)
        return text.strip()
