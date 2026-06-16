from aiogram import Router
from lentra.bot.core.intent_router import IntentRouter
from lentra.bot.features.search.handler import search_handler


def build_main_router():
    router = Router()
    intent_router = IntentRouter()

    # регистрация intents
    intent_router.register("search", search_handler)

    @router.message()
    async def default_handler(message):
        text = await intent_router.route(
            "search",
            {"message": message}
        )

        await message.answer(text or "No intent matched")

    return router
