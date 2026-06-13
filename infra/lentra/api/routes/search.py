# ============================================================
# SEARCH API ROUTE V16.4
# ============================================================

from lentra.api.services.search_service import SearchService


search_service = SearchService()


async def search_endpoint(request: dict):
    """
    Entry point for UI / Telegram / external API
    """

    return await search_service.search(request)
