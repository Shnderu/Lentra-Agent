import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from lentra.bot.handlers.router_builder import build_main_router

logging.basicConfig(level=logging.INFO)


async def main():
    logging.info("BOT STARTING")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=token)
    dp = Dispatcher()

    router = build_main_router()
    dp.include_router(router)

    logging.info("START POLLING")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
