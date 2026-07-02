import asyncio




class TelegramRuntime:
    """
    GRAPH V2 IMMUTABLE RUNTIME
    """

    def __init__(self):
        graph = build_graph()

        self.listener = graph.listener
        self.trace = graph.trace

        # router НЕ используется напрямую → только через listener
        self._running = True

    async def run(self):
        await self._run()

    async def _run(self):
        await self._cycle()

    async def _cycle(self):
        # mock event loop source (позже заменишь на telegram poller)
        while self._running:
            event = await self._fetch_event()

            processed = await self.listener.dispatch(event)

            await self.trace.emit("cycle_done", processed)

    async def _fetch_event(self):
        # stub event generator
        await asyncio.sleep(1)
        return {"type": "message", "text": "ping"}
