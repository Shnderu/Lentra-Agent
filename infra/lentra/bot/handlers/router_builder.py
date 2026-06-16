from aiogram import Router
from lentra.bot.handlers.rent_handler import setup_rent_handler


def build_main_router(container) -> Router:
    router = Router()

    rent_router = setup_rent_handler(container)
    router.include_router(rent_router)

    return router
