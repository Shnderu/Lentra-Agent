from aiogram import Router, types

from lentra.bot.features.rent_search.service import RentSearchService
from lentra.bot.features.rent_search.models import RentalSearchRequest

router = Router()
service = RentSearchService()


@router.message()
async def rent_search_handler(message: types.Message):
    text = message.text or ""

    req = RentalSearchRequest(query=text)

    result = service.search(req)

    # главное: теперь используем assistant message, а не renderer
    await message.answer(result.message)
