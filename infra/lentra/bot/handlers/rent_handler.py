from aiogram import Router
from lentra.bot.features.rent_search.service import RentSearchService

router = Router()


def setup_rent_handler(container) -> Router:
    service = RentSearchService(repository=container.rent_repository)

    @router.message()
    async def handle_rent(message):
        response = service.search(query=message.text)
        await message.answer(response)

    return router
