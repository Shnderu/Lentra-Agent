class Bot:
    def __init__(self, graph):
        self.graph = graph

    async def run(self, router):
        self.graph.add("bot", "run_start")

        # hook входа в runtime
        async for update in self._fake_stream(router):
            pass

    async def _fake_stream(self, router):
        self.graph.add("bot", "router_received")

        # просто запускаем router один раз для трассировки
        try:
            result = router.handle_test_trace()
            self.graph.add("router", "handled", result)
        except Exception as e:
            self.graph.add("router", "error", {"err": str(e)})

        self.graph.dump()

        import asyncio
        await asyncio.sleep(999999)
        yield

def build_bot(graph):
    return Bot(graph)
