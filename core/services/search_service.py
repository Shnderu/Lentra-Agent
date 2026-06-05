import logging
from core.services.flights_service import flights_service
from core.services.cache_service import cache_service


class SearchService:

    def search_flights(self, parsed: dict):
        cache_key = f"{parsed['from']}:{parsed['to']}:{parsed['date']}"

        cached = cache_service.get(cache_key)
        if cached:
            logging.info("CACHE HIT")
            return cached

        logging.info("CACHE MISS")

        result = flights_service.search(
            parsed["from"],
            parsed["to"],
            parsed["date"]
        )

        cache_service.set(cache_key, result)

        return result


search_service = SearchService()
