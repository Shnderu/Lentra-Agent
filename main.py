import asyncio
import os
from aiogram import Bot, Dispatcher
from bot.router import router

async def main():
    print(">>> FLYRUM v3.6 START")

    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
