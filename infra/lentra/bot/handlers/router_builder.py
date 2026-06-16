from aiogram import Router

from lentra.bot.core.feature_registry import FeatureRegistry
from lentra.bot.core.intent_classifier import IntentClassifier

from lentra.bot.features.manager import FeatureManager

from lentra.bot.features.search.handler import search_feature
from lentra.bot.features.fallback.handler import fallback_feature
from lentra.bot.features.base.context import FeatureContext


def build_main_router():
    router = Router()

    registry = FeatureRegistry()

    # register features
    registry.register("search", search_feature)
    registry.register("fallback", fallback_feature)

    manager = FeatureManager(registry)
    classifier = IntentClassifier()

    @router.message()
    async def handler(message):
        text = message.text or ""

        intent = classifier.classify(text)

        ctx = FeatureContext(
            message=message,
            text=text,
            intent=intent,
            meta={}
        )

        result = await manager.execute(intent, ctx)

        await message.answer(result)

    return router
