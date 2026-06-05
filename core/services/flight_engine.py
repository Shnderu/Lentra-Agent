from core.services.query_resolver import query_resolver
from core.services.kiwi_provider import kiwi_provider
from core.services.flight_provider import flight_provider
from core.services.ranking_service import ranking_service


class FlightEngine:

    def process(self, text: str):

        parsed = query_resolver.resolve(text)

        from_code = parsed["from"]
        to_code = parsed["to"]
        date = parsed["date"]

        if not from_code or not to_code:
            return None

        # 1. real API
        results = kiwi_provider.search(from_code, to_code, date)

        # 2. fallback mock
        if not results:
            results = flight_provider.search(from_code, to_code, date)

        # 3. ranking
        ranked = ranking_service.rank(results)

        return ranked


flight_engine = FlightEngine()
