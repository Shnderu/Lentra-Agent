from lentra.core.runtime_trace_v1 import RuntimeTraceV1

trace = RuntimeTraceV1()


def trace_event(node: str, event: str, payload=None):
    return trace.emit(node, event, payload or {})
