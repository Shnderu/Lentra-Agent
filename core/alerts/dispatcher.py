
from aiogram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


async def send_notification(user_id: int, event: dict):

    text = (
        "✈️ FlyRum Alert\n\n"
        f"Цена: {event['price']}\n"
        f"События: {', '.join(event['triggers'])}"
    )

    await bot.send_message(chat_id=user_id, text=text)
