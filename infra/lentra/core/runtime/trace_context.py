import uuid
from datetime import datetime


class TraceContext:

    def __init__(self, trace_id: str = None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.started_at = datetime.utcnow().isoformat()

    def child(self, layer: str, event: str):
        return f"{self.trace_id}:{layer}.{event}"
