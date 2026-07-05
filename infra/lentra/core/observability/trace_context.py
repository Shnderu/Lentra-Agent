import uuid
import time
from contextvars import ContextVar
from typing import Optional, Dict, Any

_trace_context: ContextVar[Optional[Dict[str, Any]]] = ContextVar("trace_context", default=None)


def new_request_id() -> str:
    return str(uuid.uuid4())


def init_trace(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create or reuse request trace
    """
    trace = {
        "request_id": payload.get("request_id") or new_request_id(),
        "timestamp": time.time(),
        "payload": payload,
    }
    _trace_context.set(trace)
    return trace


def get_trace() -> Optional[Dict[str, Any]]:
    return _trace_context.get()


def attach_trace(data: Dict[str, Any]) -> Dict[str, Any]:
    trace = get_trace()
    if not trace:
        return data

    return {
        **data,
        "request_id": trace["request_id"],
        "timestamp": trace["timestamp"],
    }
