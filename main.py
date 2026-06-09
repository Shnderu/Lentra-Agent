import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.runtime.unified import unified_entry
from core.fsm.context import set_state

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()

dp.include_router(router)


@router.message(CommandStart())
async def start_handler(message: Message):

    user_id = message.from_user.id

    set_state(user_id, "route_from")

    print("[START] FSM -> route_from")

    await message.answer("✈️ Откуда вылет?")


@router.message()
async def all_messages(message: Message):

    print("🔥 PIPELINE INPUT:", message.text)

    result = await unified_entry(message)

    print("🔥 PIPELINE OUTPUT:", result)

    if result:
        await message.answer(str(result))
    else:
        await message.answer("🤖 fallback")


async def main():
    print(">>> FLYRUM FULL PIPELINE ACTIVE")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
