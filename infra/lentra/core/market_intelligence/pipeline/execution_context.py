class ExecutionContext:
    def __init__(self, orchestrator):
        if not hasattr(orchestrator, "execute"):
            raise RuntimeError("Invalid orchestrator injected: missing execute()")

        self.orchestrator = orchestrator
