import os
import asyncio

from aiogram import Bot, Dispatcher
from core.router.router import router


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():

    print(">>> FLYRUM START")

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    print(">>> ROUTER LOADED")
    print(">>> START POLLING")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
