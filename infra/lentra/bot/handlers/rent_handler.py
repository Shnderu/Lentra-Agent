from aiogram import Router, F
from aiogram.types import Message

from lentra.bot.features.base.context import FeatureContext
from lentra.application.rent_search.service import (
    RentSearchApplicationService
)


router = Router()

service = RentSearchApplicationService()


def setup_rent_handler(container) -> Router:
    global service

    service = container.rent_search_service

    return router


@router.message(F.text)
async def handle_rent(message: Message):

    ctx = FeatureContext(
        message=message,
        text=message.text,
        intent="rent_search",
        meta={
            "user_id": message.from_user.id
        }
    )

    result = await service.search(
        {
            "text": ctx.text,
            "intent": ctx.intent,
            "meta": ctx.meta
        }
    )

    await message.answer(
        str(result)
    )
