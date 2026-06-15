from datetime import datetime

from lentra.bot.notifications.core.model import Notification
from lentra.bot.notifications.services.dispatcher import NotificationDispatcher
from lentra.bot.events.registry import bus


class NotificationEngine:

    def __init__(self, dispatcher: NotificationDispatcher):
        self.dispatcher = dispatcher

    async def notify(self, user_id: int, ntype: str, payload: dict):

        notification = Notification(
            user_id=user_id,
            type=ntype,
            payload=payload,
            created_at=datetime.utcnow()
        )

        await self.dispatcher.send(notification)


def register_notification_hooks(engine: NotificationEngine):

    async def on_search_completed(event):

        if event.payload.get("results_count", 0) == 0:

            await engine.notify(
                event.user_id,
                "no_results",
                {"query": event.payload.get("query")}
            )

    bus.subscribe("search_completed", on_search_completed)
