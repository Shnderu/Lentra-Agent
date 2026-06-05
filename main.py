import asyncio
import os
import logging

from aiogram import Bot, Dispatcher
from bot.router import router

logging.basicConfig(level=logging.INFO)


async def main():
    print(">>> FLYRUM v3.6 START")

    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN missing")

    bot = Bot(token=token)

    dp = Dispatcher()
    dp.include_router(router)

    print(">>> ROUTER LOADED")
    print(">>> START POLLING")

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
