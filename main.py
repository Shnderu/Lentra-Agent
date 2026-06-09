
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery

from core.runtime.unified import unified_entry

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# -------------------------
# UNIFIED MESSAGE PIPELINE
# -------------------------
@dp.message()
async def handle_message(message: Message):
    result = await unified_entry(message)
    if result:
        await message.answer(str(result))


# -------------------------
# CALLBACK PIPELINE
# -------------------------
@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    result = await unified_entry(callback)

    if result:
        await callback.message.answer(str(result))

    await callback.answer()


async def main():
    print(">>> FLYRUM UNIFIED RUNTIME v1 START")
    print(">>> HANDLERS ATTACHED")
    print(">>> START POLLING")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
