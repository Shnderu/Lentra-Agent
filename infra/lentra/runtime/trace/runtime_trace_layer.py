class RuntimeTraceLayer:
    """
    Runtime-only observability collector.

    NEVER imported by core.
    """

    def __init__(self):
        self.buffer = []

    def emit(self, event: dict):
        self.buffer.append(event)

    def flush(self):
        return self.buffer
