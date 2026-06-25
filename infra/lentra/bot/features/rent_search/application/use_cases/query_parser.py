import re
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class QueryParser:
    """
    Преобразует сырой текст в структурированный SearchContext
    """

    CITY_ALIASES = {
        "da nang": "da_nang",
        "danang": "da_nang",
        "nha trang": "nha_nang",
        "ho chi minh": "ho_chi_minh",
        "saigon": "ho_chi_minh",
        "hanoi": "hanoi",
        "bangkok": "bangkok",
        "phuket": "phuket",
        "chiang mai": "chiang_mai",
    }

    COUNTRY_ALIASES = {
        "thailand": "thailand",
        "vietnam": "vietnam",
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
        cities = list(self.CITY_ALIASES.keys())

        for c in cities:
            if c in text:
                return self.CITY_ALIASES[c]

        return None

    def _extract_country(self, text: str):
        countries = list(self.COUNTRY_ALIASES.keys())

        for c in countries:
            if c in text:
                return self.COUNTRY_ALIASES[c]

        # fallback: если есть city → infer country минимально
        if "da_nang" in text or "ho_chi_minh" in text or "hanoi" in text:
            return "vietnam"

        return None

    def _extract_price(self, text: str):
        match = re.search(r"(\d+)\s*-\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def _clean(self, text: str) -> str:
        text = re.sub(r"\d+\s*-\s*\d+", "", text)
        return text.strip()
