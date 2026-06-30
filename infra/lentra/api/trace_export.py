from fastapi import APIRouter

from lentra.core.runtime_trace_registry import TraceRegistry

router = APIRouter()

registry = TraceRegistry()


@router.get("/trace/export")
def export_traces():
    """
    Returns full runtime execution graph (v1)
    """
    return registry.export_all()


@router.get("/trace/list")
def list_traces():
    return {
        "trace_ids": list(registry.traces.keys())
    }
