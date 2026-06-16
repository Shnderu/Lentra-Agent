from aiogram import Router
from lentra.bot.features.rent_search.service import RentSearchService

router = Router()

def build_rent_handler(container):
    service = container.rent_search_service

    @router.message()
    async def handle_rent(message):
        result = await service.search(message.text)
        return result

    return router
