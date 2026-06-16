from aiogram import Router

from lentra.bot.features.registry.init import build_feature_registry
from lentra.bot.handlers.rent_handler import router as rent_router


def build_main_router(container) -> Router:
    router = Router()

    feature_registry = build_feature_registry(container)

    # inject registry into container (light pattern)
    container.feature_registry = feature_registry

    router.include_router(rent_router)

    return router
