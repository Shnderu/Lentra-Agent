from fastapi import APIRouter

router = APIRouter()

_last_trace = None


def set_trace(trace):
    global _last_trace
    _last_trace = trace


@router.get("/debug/trace")
def get_trace():
    return _last_trace if _last_trace else {"trace": "empty"}
