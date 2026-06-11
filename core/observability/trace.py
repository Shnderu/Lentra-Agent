import uuid
import time

class TraceContext:
    """
    Lightweight distributed tracing context
    """

    def __init__(self, trace_id=None):
        self.trace_id = trace_id or str(uuid.uuid4())
        self.span_id = str(uuid.uuid4())
        self.created_at = time.time()

    def child(self):
        return TraceContext(self.trace_id)
