import time
import uuid


def start_span(trace_id: str, name: str):
    return {
        "span_id": str(uuid.uuid4()),
        "trace_id": trace_id,
        "name": name,
        "start": time.time(),
    }


def end_span(span: dict):
    span["end"] = time.time()
    span["duration_ms"] = (span["end"] - span["start"]) * 1000
    return span
