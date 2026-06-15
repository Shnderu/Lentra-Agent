import asyncio
import logging

from aiogram import Bot, Dispatcher

from lentra.bot.config import BOT_TOKEN
from lentra.bot.handlers.router_builder import build_main_router


logging.basicConfig(level=logging.INFO)


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is empty")

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # IMPORTANT: single router build point
    router = build_main_router()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
