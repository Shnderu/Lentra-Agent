import asyncio


class EventBusSafe:

    def __init__(self, bus):
        self.bus = bus

    def publish(self, event_type, payload):
        try:
            coro = self.bus.publish(event_type, payload)

            if asyncio.iscoroutine(coro):
                asyncio.create_task(coro)
            else:
                return coro

        except Exception as e:
            # visibility must NEVER crash pipeline
            print(f"[EVENT BUS ERROR] {e}")
