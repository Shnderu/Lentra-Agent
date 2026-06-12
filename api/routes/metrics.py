from fastapi import APIRouter
from core.redis import get_redis

router = APIRouter()


@router.get("/metrics")
def metrics():
    r = get_redis()

    keys = r.keys("metrics:*")

    lines = []

    for k in keys:
        value = r.get(k)
        name = k.replace("metrics:", "")
        lines.append(f"{name} {value}")

    return "\n".join(lines)
