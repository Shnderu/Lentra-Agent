
from aiogram import Router
from aiogram.filters import Command

router = Router()

# SYSTEM COMMANDS (optional fallback only, NOT catch-all)

@router.message(Command("ping"))
async def ping(message):
    await message.answer("pong")

