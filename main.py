import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from core.runtime.unified import unified_entry
from core.ui.screens.home import show_home

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await show_home(message)


@dp.message(Command('help'))
async def help_cmd(message: Message):
    await message.answer('FlyRum AI: /start → menu')


@dp.message()
async def all_messages(message: Message):
    result = await unified_entry(message)
    if result:
        await message.answer(str(result))


@dp.callback_query()
async def callbacks(callback: CallbackQuery):
    result = await unified_entry(callback)
    if result:
        await callback.message.answer(str(result))
    await callback.answer()


async def main():
    print('>>> FLYRUM FIXED RUNTIME START')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
