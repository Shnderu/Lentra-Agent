import os
from aiogram import Bot
from core.worker.handlers.base import BaseHandler


class NotifyHandler(BaseHandler):

    def __init__(self):
        self.bot = Bot(token=os.getenv("BOT_TOKEN"))

    async def handle(self, task_id: int, payload: dict):
        user_id = payload.get("user_id")
        text = payload.get("text", "")

        if not user_id:
            raise ValueError("Missing user_id")

        await self.bot.send_message(user_id, f"[NOTIFY] {text}")

        return {
            "task_id": task_id,
            "status": "notified"
        }
