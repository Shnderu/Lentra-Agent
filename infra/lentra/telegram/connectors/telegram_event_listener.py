class TelegramEventListener:
    """
    TRACE GRAPH V2 EVENT ADAPTER (IMMUTABLE)
    """

    def __init__(self, router, trace):
        self.router = router
        self.trace = trace

    async def next_event(self):
        return {}

    async def handle_event(self, event: dict):
        # NO ASYNC ROUTING HERE
        return event
