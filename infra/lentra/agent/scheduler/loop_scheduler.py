# ============================================================
# LOOP SCHEDULER V17.1
# ============================================================

import asyncio


class LoopScheduler:
    def __init__(self, loop_engine):
        self.loop_engine = loop_engine
        self.subscriptions = []

    def subscribe(self, query):
        self.subscriptions.append(query)

    async def start(self):
        while True:
            for q in self.subscriptions:
                await self.loop_engine.run_cycle(q)

            await asyncio.sleep(60)
