from aiogram import Router, F
from aiogram.types import Message

from lentra.bot.features.base.context import FeatureContext


router = Router()


def setup_rent_handler(container) -> Router:

    return router


@router.message(F.text)
async def handle_rent(message: Message):

    container = getattr(
        router,
        "container",
        None
    )

    if container is None:
        await message.answer(
            "Runtime container not initialized"
        )
        return

    ctx = FeatureContext(
        message=message,
        text=message.text,
        intent="rent_search",
        meta={
            "user_id": message.from_user.id
        }
    )

    result = await container.rent_search_service.search(
        {
            "text": ctx.text,
            "intent": ctx.intent,
            "meta": ctx.meta
        }
    )

    await message.answer(
        str(result)
    )
