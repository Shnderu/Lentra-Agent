from aiogram import Router, F
from aiogram.types import Message

from lentra.bot.features.base.context import FeatureContext
from lentra.bot.features.rent_search.handler import RentSearchHandler

router = Router()

handler = RentSearchHandler()


def setup_rent_handler(container) -> Router:
    return router


@router.message(F.text)
async def handle_rent(message: Message):

    ctx = FeatureContext(
        text=message.text,
        user_id=message.from_user.id
    )

    response = await handler.handle(ctx)

    await message.answer(response)
