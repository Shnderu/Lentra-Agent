from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("FlyRum AI started 🚀")


@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("Available commands: /start /help")


@router.message()
async def fallback(message: Message):
    await message.answer("⚠️ Command not recognized")
