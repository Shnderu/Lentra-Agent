from lentra.core.market_intelligence.gateway.intelligence_gateway import IntelligenceGateway


class WorkerLoop:
    def __init__(self):
        # единая точка входа через gateway (v2 compliant)
        self.gateway = IntelligenceGateway()

    def process_event(self, event: dict):
        """
        Worker event processing (ARCH LOCK v2 compliant)
        """
        return self.gateway.interpret(event)


# backward-compatible entrypoint
_worker = WorkerLoop()


def process_event(event):
    return _worker.process_event(event)
