from aiogram import Router

from lentra.bot.handlers.handlers import build_message_router
from lentra.bot.handlers.callbacks import build_callback_router


def build_main_router(container) -> Router:
    router = Router()

    router.include_router(build_message_router(container))
    router.include_router(build_callback_router(container))

    return router
