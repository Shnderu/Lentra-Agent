from fastapi import APIRouter
from lentra.api.pipeline import replay_engine

router = APIRouter(prefix="/admin")

@router.get("/replay/{request_id}")
def replay(request_id: str):
    return replay_engine.replay(request_id)
