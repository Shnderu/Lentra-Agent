import os
from aiogram import Bot
from core.worker.handlers.base import BaseHandler


class SendMessageHandler(BaseHandler):

    def __init__(self):
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))

    async def handle(self, task_id: int, payload: dict):
        user_id = payload.get("user_id")
        text = payload.get("text")

        if not user_id or not text:
            raise ValueError("Invalid send_message payload")

        await self.bot.send_message(user_id, text)

        return {
            "task_id": task_id,
            "status": "sent"
        }
