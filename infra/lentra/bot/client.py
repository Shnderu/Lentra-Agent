class BotClient:
    def __init__(self):
        pass

    async def start(self):
        print("BOT STARTED (UI LAYER ONLY)")

        while True:
            await self._poll()

    async def _poll(self):
        import asyncio
        await asyncio.sleep(1)

        # simulated event
        trace_id = "ui-" + str(__import__("uuid").uuid4())

        print(f"[BOT TRACE] {trace_id} | polling events")
