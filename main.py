import os
import asyncio

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message


BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN missing")


bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
router = Router()


# -------------------------
# HANDLERS
# -------------------------
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("FlyRum AI is running 🚀")


# -------------------------
# MAIN
# -------------------------
async def main():
    print(">>> FLYRUM v3.6 START")

    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    print(">>> ROUTER LOADED")
    print(">>> START POLLING")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
