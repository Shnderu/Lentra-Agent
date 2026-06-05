import re


class QueryResolver:

    def resolve(self, text: str) -> dict:
        text = text.lower()

        # простой NLP слой (пока без LLM API)
        return {
            "from": self._find_city(text, ["москва", "питер", "санкт-петербург"]),
            "to": self._find_city(text, ["стамбул", "дубай", "анталия"]),
            "date": self._extract_date(text),
            "raw": text
        }

    def _find_city(self, text, cities):
        for c in cities:
            if c in text:
                return c.upper()
        return None

    def _extract_date(self, text):
        match = re.search(r"(\d{1,2})\s?(июл|июня|авг|августа)", text)
        return match.group(0) if match else None


query_resolver = QueryResolver()
