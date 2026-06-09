import os
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)


async def send_message(user_id: int, text: str):
    await bot.send_message(chat_id=user_id, text=text)
