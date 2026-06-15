from aiogram import Bot
from lentra.bot.notifications.core.model import Notification


class NotificationDispatcher:

    def __init__(self, bot: Bot):
        self.bot = bot

    async def send(self, notification: Notification):

        if notification.type == "price_drop":

            text = (
                f"🔥 Price drop detected!\n\n"
                f"New price: {notification.payload.get('price')} mln VND\n"
                f"City: {notification.payload.get('city')}"
            )

        elif notification.type == "new_match":

            text = (
                f"🏡 New match found!\n\n"
                f"{notification.payload.get('title')}"
            )

        else:
            text = str(notification.payload)

        await self.bot.send_message(notification.user_id, text)
