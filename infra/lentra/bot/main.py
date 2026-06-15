import asyncio
from aiogram import Bot, Dispatcher

from lentra.bot.config import BOT_TOKEN
from lentra.bot.core.container import build_container

from lentra.bot.handlers.handlers import build_main_router
from lentra.bot.handlers.filters import build_filters_router
from lentra.bot.handlers.callbacks import build_callbacks_router
from lentra.bot.handlers.tracking import build_tracking_router


async def main():

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    container = build_container()

    dp.include_router(build_main_router(container))
    dp.include_router(build_filters_router())
    dp.include_router(build_callbacks_router())
    dp.include_router(build_tracking_router())

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
