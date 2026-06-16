from aiogram import Router

from lentra.bot.handlers.rent_handler import router as rent_router


def build_main_router(container) -> Router:
    router = Router()

    # RENT FEATURE (primary path)
    router.include_router(rent_router)

    return router
