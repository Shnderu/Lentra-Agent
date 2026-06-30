class RuntimeTraceAudit:
    """
    READ-ONLY execution tracer (v1)
    Does NOT modify pipeline execution.
    Only observes runtime graph flow.
    """

    def __init__(self):
        self.events = []

    def log(self, event: str, meta=None):
        self.events.append({
            "event": event,
            "meta": meta or {}
        })

    def dump(self):
        return self.events
