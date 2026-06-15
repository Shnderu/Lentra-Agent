from aiogram import Router

from lentra.bot.handlers.filters import router as filters_router
from lentra.bot.handlers.callbacks import router as callbacks_router
from lentra.bot.handlers.tracking import router as tracking_router
from lentra.bot.handlers.handlers import router as message_router


def build_main_router() -> Router:
    router = Router()

    # IMPORTANT: order matters (UX → callbacks → tracking → messages)
    router.include_router(filters_router)
    router.include_router(callbacks_router)
    router.include_router(tracking_router)
    router.include_router(message_router)

    return router
