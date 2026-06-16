import re
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class QueryParser:
    """
    Преобразует сырой текст в структурированный SearchContext
    """

    def parse(self, raw_query: str) -> SearchContext:
        query = raw_query.lower().strip()

        city = self._extract_city(query)
        min_price, max_price = self._extract_price(query)

        cleaned_query = self._clean(query)

        return SearchContext(
            raw_query=raw_query,
            query=cleaned_query,
            city=city,
            min_price=min_price,
            max_price=max_price
        )

    def _extract_city(self, text: str):
        # минимальная заготовка (расширим позже)
        cities = ["hanoi", "saigon", "bangkok", "phuket"]
        for c in cities:
            if c in text:
                return c
        return None

    def _extract_price(self, text: str):
        match = re.search(r"(\d+)\s*-\s*(\d+)", text)
        if match:
            return int(match.group(1)), int(match.group(2))
        return None, None

    def _clean(self, text: str) -> str:
        text = re.sub(r"\d+\s*-\s*\d+", "", text)
        return text.strip()
