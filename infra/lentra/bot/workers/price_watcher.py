import asyncio
from lentra.bot.events.registry import bus


class PriceWatcher:

    def __init__(self):
        self.last_prices = {}

    async def run(self):

        while True:

            await asyncio.sleep(10)

            # MOCK: здесь позже будет API poll / db diff
            fake_event = {
                "user_id": 1,
                "price": 5.2,
                "city": "Da Nang"
            }

            await bus.emit(
                type("Event", (), {
                    "type": "price_drop",
                    "user_id": 1,
                    "payload": fake_event,
                    "timestamp": None
                })
            )
