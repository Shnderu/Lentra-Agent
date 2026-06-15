from typing import List, Callable, Dict
from lentra.bot.events.types.base import Event


class EventBus:

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):

        if event_type not in self.subscribers:
            self.subscribers[event_type] = []

        self.subscribers[event_type].append(handler)

    async def emit(self, event: Event):

        handlers = self.subscribers.get(event.type, [])

        for handler in handlers:
            await handler(event)
