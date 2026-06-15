from lentra.bot.events.bus.bus import EventBus
from lentra.bot.events.types.domain import create_event


class EventEmitter:

    def __init__(self, bus: EventBus):
        self.bus = bus

    async def emit(self, event_type: str, user_id: int, payload: dict):

        event = create_event(event_type, user_id, payload)

        await self.bus.emit(event)
