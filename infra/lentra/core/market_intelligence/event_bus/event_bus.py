from collections import defaultdict
from typing import Callable, Dict, List, Any
import asyncio


class EventBus:

    def __init__(self, event_log=None):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.event_log = event_log

    def subscribe(self, event_type: str, handler: Callable):
        self._subscribers[event_type].append(handler)

    async def _publish_async(self, event_type: str, event: dict):

        if self.event_log:
            self.event_log.append(event)

        handlers = self._subscribers.get(event_type, [])

        for handler in handlers:
            if asyncio.iscoroutinefunction(handler):
                await handler(event)
            else:
                handler(event)

    def publish(self, event_type: str, event: dict):
        """
        SAFE SYNC ENTRYPOINT
        """

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._publish_async(event_type, event))
        except RuntimeError:
            # no event loop → fallback sync
            asyncio.run(self._publish_async(event_type, event))
