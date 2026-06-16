from aiogram import Router

from lentra.bot.core.feature_registry import FeatureRegistry
from lentra.bot.core.intent_router import IntentRouter

from lentra.bot.features.search.handler import search_feature
from lentra.bot.features.fallback.handler import fallback_feature


def build_main_router():
    router = Router()

    registry = FeatureRegistry()

    # register features
    registry.register("search", search_feature)
    registry.register("fallback", fallback_feature)

    intent_router = IntentRouter(registry)

    @router.message()
    async def default_handler(message):
        text = await intent_router.route(
            "search",
            {"message": message}
        )

        await message.answer(text)

    return router
